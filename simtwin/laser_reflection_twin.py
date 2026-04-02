#!/usr/bin/env python3
import argparse
import json
import logging
import math
import os
import signal
import threading
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Union


@dataclass
class BeamShape:
    peak_num_x: int
    peak_num_y: int
    peak_step_x: int
    peak_step_y: int
    peak_width_x: int
    peak_width_y: int


@dataclass
class MirrorGeometry:
    detector_distance_m: float
    pixel_size_um: float
    detector_width_px: int
    detector_height_px: int
    center_x_px: float
    center_y_px: float
    offset_x_px: float
    offset_y_px: float
    mirror_matrix_rad_per_unit: list[list[float]]


@dataclass
class TwinConfig:
    protocol: str
    update_period_s: float
    motor_x_pv: str
    motor_y_pv: str
    camera_base_pv: str
    mirror_geometry: MirrorGeometry
    beam_shape: BeamShape

    @classmethod
    def from_file(cls, path: str) -> "TwinConfig":
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)

        motor_x_pv = _normalize_motor_pv(os.environ.get("MOTX") or raw["motor_x_pv"])
        motor_y_pv = _normalize_motor_pv(os.environ.get("MOTY") or raw["motor_y_pv"])
        camera_base_pv = os.environ.get("CAM") or raw["camera_base_pv"]

        geometry = raw["mirror_geometry"]
        shape = raw["beam_shape"]
        return cls(
            protocol=raw.get("protocol", "ca"),
            update_period_s=float(raw.get("update_period_s", 0.05)),
            motor_x_pv=motor_x_pv,
            motor_y_pv=motor_y_pv,
            camera_base_pv=camera_base_pv.rstrip(":"),
            mirror_geometry=MirrorGeometry(
                detector_distance_m=float(geometry["detector_distance_m"]),
                pixel_size_um=float(geometry["pixel_size_um"]),
                detector_width_px=int(geometry["detector_width_px"]),
                detector_height_px=int(geometry["detector_height_px"]),
                center_x_px=float(geometry["center_x_px"]),
                center_y_px=float(geometry["center_y_px"]),
                offset_x_px=float(geometry.get("offset_x_px", 0.0)),
                offset_y_px=float(geometry.get("offset_y_px", 0.0)),
                mirror_matrix_rad_per_unit=geometry["mirror_matrix_rad_per_unit"],
            ),
            beam_shape=BeamShape(
                peak_num_x=int(shape.get("peak_num_x", 1)),
                peak_num_y=int(shape.get("peak_num_y", 1)),
                peak_step_x=int(shape.get("peak_step_x", 0)),
                peak_step_y=int(shape.get("peak_step_y", 0)),
                peak_width_x=int(shape.get("peak_width_x", 40)),
                peak_width_y=int(shape.get("peak_width_y", 40)),
            ),
        )


def _normalize_motor_pv(pv_name: str) -> str:
    pv_name = pv_name.strip()
    if '.' in pv_name:
        return pv_name
    return f"{pv_name}.RBV"


class PyEpicsBackend:
    def __init__(self) -> None:
        try:
            import epics  # type: ignore
        except ImportError as exc:
            raise RuntimeError("pyepics is required in the runtime image") from exc
        self._epics = epics
        self._pvs: Dict[str, object] = {}
        self._monitors: list[object] = []

    def get(self, pv_name: str) -> float:
        value = self._epics.caget(pv_name, timeout=2.0)
        if value is None:
            raise RuntimeError(f"failed to read PV {pv_name}")
        return float(value)

    def put(self, pv_name: str, value: Union[float, int]) -> None:
        ok = self._epics.caput(pv_name, value, wait=False, timeout=2.0)
        if ok is None:
            raise RuntimeError(f"failed to write PV {pv_name}")

    def monitor(self, pv_name: str, callback: Callable[[str, float], None]) -> None:
        pv = self._epics.PV(
            pv_name,
            auto_monitor=True,
            callback=lambda pvname=None, value=None, **_: self._dispatch(callback, pvname or pv_name, value),
        )
        self._pvs[pv_name] = pv
        self._monitors.append(pv)

    @staticmethod
    def _dispatch(callback: Callable[[str, float], None], pv_name: str, value: object) -> None:
        if value is None:
            return
        callback(pv_name, float(value))


class P4PBackend:
    def __init__(self) -> None:
        try:
            from p4p.client.thread import Context  # type: ignore
        except ImportError as exc:
            raise RuntimeError("p4p is required in the runtime image") from exc
        self._context = Context("pva")
        self._subscriptions = []

    def get(self, pv_name: str) -> float:
        value = self._context.get(pv_name, timeout=2.0)
        return self._coerce_scalar(value)

    def put(self, pv_name: str, value: Union[float, int]) -> None:
        self._context.put(pv_name, value, wait=False, timeout=2.0)

    def monitor(self, pv_name: str, callback: Callable[[str, float], None]) -> None:
        sub = self._context.monitor(
            pv_name,
            lambda value: self._dispatch(callback, pv_name, value),
            notify_disconnect=True,
        )
        self._subscriptions.append(sub)

    @staticmethod
    def _coerce_scalar(value: object) -> float:
        if value is None:
            raise RuntimeError("disconnected PVA monitor")
        if hasattr(value, "value"):
            value = getattr(value, "value")
        if isinstance(value, dict) and "value" in value:
            value = value["value"]
        return float(value)

    @classmethod
    def _dispatch(cls, callback: Callable[[str, float], None], pv_name: str, value: object) -> None:
        try:
            callback(pv_name, cls._coerce_scalar(value))
        except Exception:
            return


class MirrorToBeamModel:
    def __init__(self, geometry: MirrorGeometry, shape: BeamShape) -> None:
        self._geometry = geometry
        self._shape = shape

    def evaluate(self, motor_x: float, motor_y: float) -> Dict[str, int]:
        matrix = self._geometry.mirror_matrix_rad_per_unit
        mirror_angle_x = (matrix[0][0] * motor_x) + (matrix[0][1] * motor_y)
        mirror_angle_y = (matrix[1][0] * motor_x) + (matrix[1][1] * motor_y)

        pixel_size_m = self._geometry.pixel_size_um * 1e-6
        beam_offset_x_px = (2.0 * self._geometry.detector_distance_m * math.tan(mirror_angle_x)) / pixel_size_m
        beam_offset_y_px = (2.0 * self._geometry.detector_distance_m * math.tan(mirror_angle_y)) / pixel_size_m

        center_x = self._geometry.center_x_px + self._geometry.offset_x_px + beam_offset_x_px
        center_y = self._geometry.center_y_px + self._geometry.offset_y_px + beam_offset_y_px

        start_x = int(round(center_x - (self._shape.peak_width_x / 2.0)))
        start_y = int(round(center_y - (self._shape.peak_width_y / 2.0)))

        max_x = max(0, self._geometry.detector_width_px - self._shape.peak_width_x)
        max_y = max(0, self._geometry.detector_height_px - self._shape.peak_width_y)
        start_x = min(max(start_x, 0), max_x)
        start_y = min(max(start_y, 0), max_y)

        return {
            "PeakStartX": start_x,
            "PeakStartY": start_y,
            "PeakNumX": self._shape.peak_num_x,
            "PeakNumY": self._shape.peak_num_y,
            "PeakStepX": self._shape.peak_step_x,
            "PeakStepY": self._shape.peak_step_y,
            "PeakWidthX": self._shape.peak_width_x,
            "PeakWidthY": self._shape.peak_width_y,
        }


class AreaDetectorOutput:
    CAMERA_FIELDS = (
        "PeakStartX",
        "PeakStartY",
        "PeakNumX",
        "PeakNumY",
        "PeakStepX",
        "PeakStepY",
        "PeakWidthX",
        "PeakWidthY",
    )

    def __init__(self, backend: PyEpicsBackend, camera_base_pv: str) -> None:
        self._backend = backend
        self._camera_base_pv = camera_base_pv.rstrip(":")
        self._last_written: Dict[str, int] = {}

    def write(self, beam: Dict[str, int]) -> None:
        for field in self.CAMERA_FIELDS:
            value = int(beam[field])
            if self._last_written.get(field) == value:
                continue
            self._backend.put(f"{self._camera_base_pv}:{field}", value)
            self._last_written[field] = value


class DigitalTwinApplication:
    def __init__(self, config: TwinConfig, backend: PyEpicsBackend) -> None:
        self._config = config
        self._backend = backend
        self._model = MirrorToBeamModel(config.mirror_geometry, config.beam_shape)
        self._output = AreaDetectorOutput(backend, config.camera_base_pv)
        self._lock = threading.Lock()
        self._motor_values = {config.motor_x_pv: 0.0, config.motor_y_pv: 0.0}
        self._dirty = threading.Event()
        self._running = True

    def start(self) -> None:
        self._motor_values[self._config.motor_x_pv] = self._wait_for_value(self._config.motor_x_pv)
        self._motor_values[self._config.motor_y_pv] = self._wait_for_value(self._config.motor_y_pv)
        self._backend.monitor(self._config.motor_x_pv, self._on_motor_update)
        self._backend.monitor(self._config.motor_y_pv, self._on_motor_update)
        self._dirty.set()

    def stop(self) -> None:
        self._running = False
        self._dirty.set()

    def run_forever(self) -> None:
        while self._running:
            self._dirty.wait(self._config.update_period_s)
            self._dirty.clear()
            if not self._running:
                break
            self._apply_update()

    def _on_motor_update(self, pv_name: str, value: float) -> None:
        with self._lock:
            self._motor_values[pv_name] = value
        self._dirty.set()

    def _apply_update(self) -> None:
        with self._lock:
            motor_x = self._motor_values[self._config.motor_x_pv]
            motor_y = self._motor_values[self._config.motor_y_pv]
        beam = self._model.evaluate(motor_x, motor_y)
        try:
            self._output.write(beam)
        except Exception as exc:
            logging.warning("camera update failed: %s", exc)

    def _wait_for_value(self, pv_name: str, timeout_s: float = 120.0) -> float:
        deadline = time.time() + timeout_s
        while self._running and time.time() < deadline:
            try:
                return self._backend.get(pv_name)
            except Exception as exc:
                logging.info("waiting for PV %s: %s", pv_name, exc)
                time.sleep(1.0)
        raise RuntimeError(f"timeout waiting for PV {pv_name}")


def build_backend(protocol: str) -> object:
    protocol = protocol.lower()
    if protocol == "ca":
        return PyEpicsBackend()
    if protocol == "pva":
        return P4PBackend()
    raise ValueError(f"unsupported protocol '{protocol}': use 'ca' or 'pva'")


def dump_pv_list(path: str, config: TwinConfig) -> None:
    pv_names = [
        config.motor_x_pv,
        config.motor_y_pv,
    ]
    pv_names.extend(f"{config.camera_base_pv}:{field}" for field in AreaDetectorOutput.CAMERA_FIELDS)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(pv_names) + "\n")


def main() -> int:
    logging.basicConfig(level=os.environ.get("SIMTWIN_LOG_LEVEL", "INFO"))
    parser = argparse.ArgumentParser(description="Laser reflection digital twin driving an areaDetector SimDetector")
    parser.add_argument("--config", required=True, help="Path to the digital twin JSON configuration")
    parser.add_argument("--pvout", default="pvlist.txt", help="Path where the list of input/output PVs will be written")
    args = parser.parse_args()

    config = TwinConfig.from_file(args.config)
    backend = build_backend(config.protocol)
    app = DigitalTwinApplication(config, backend)

    dump_pv_list(args.pvout, config)

    def _handle_signal(_signum: int, _frame: object) -> None:
        app.stop()

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    app.start()
    app.run_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())