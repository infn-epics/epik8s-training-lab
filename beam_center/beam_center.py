#!/usr/bin/env python3
"""
Soft IOC – closed-loop beam centering on overlay 1.

Reads the beam centroid from the camera stats plugin and the overlay-1
rectangle position, then iteratively drives two motors (X, Y) to bring
the beam centroid into the center of the overlay rectangle.

Exposed PVs (under --prefix):
  - gain_x, gain_y : proportional gain  px → motor-units  (default 0.01)
  - tolerance      : convergence threshold in pixels       (default 5)
  - interval       : loop period in seconds                (default 1.0)
  - errX, errY     : last measured error in pixels         (read-only)
  - status         : descriptive text                      (read-only)
  - start          : command button – begin centering loop
  - stop           : command button – abort centering loop
"""
import argparse
import logging
import os
import threading
import time

from p4p.client.thread import Context  # type: ignore

log = logging.getLogger("beam_center")


def dump_pvs(softioc_module, output_path: str) -> None:
    """Dump IOC PV names to a file using softioc.dbl()."""
    with open(output_path, "w", encoding="utf-8") as handle:
        old_stdout = os.dup(1)
        os.dup2(handle.fileno(), 1)
        try:
            softioc_module.dbl()
        finally:
            os.dup2(old_stdout, 1)
            os.close(old_stdout)


# ── helpers ─────────────────────────────────────────────────────────

def _coerce_scalar(value) -> float:
    if value is None:
        raise RuntimeError("disconnected PVA value")
    if hasattr(value, "value"):
        value = getattr(value, "value")
    if isinstance(value, dict) and "value" in value:
        value = value["value"]
    return float(value)


def _caget(context: Context, pv: str) -> float:
    return _coerce_scalar(context.get(pv, timeout=2.0))


def _caput(context: Context, pv: str, value, wait: bool = True) -> None:
    context.put(pv, value, wait=wait, timeout=5.0)


def read_overlay_center(context: Context, cam: str) -> tuple[float, float]:
    """Return the center (px) of overlay slot 1."""
    px = _caget(context, f"{cam}:Overlay1:1:PositionX_RBV")
    py = _caget(context, f"{cam}:Overlay1:1:PositionY_RBV")
    sx = _caget(context, f"{cam}:Overlay1:1:SizeX_RBV")
    sy = _caget(context, f"{cam}:Overlay1:1:SizeY_RBV")
    return px + sx / 2.0, py + sy / 2.0


def read_beam_centroid(context: Context, cam: str) -> tuple[float, float]:
    """Return beam centroid from the base Stats1 plugin."""
    cx = _caget(context, f"{cam}:Stats1:CentroidX_RBV")
    cy = _caget(context, f"{cam}:Stats1:CentroidY_RBV")
    return cx, cy


def ensure_centroid_enabled(context: Context, cam: str) -> None:
    _caput(context, f"{cam}:Stats1:ComputeCentroid", 1)


def move_motor(context: Context, motor_pv: str, delta: float) -> None:
    """Issue a relative move by writing new absolute position."""
    current = _caget(context, f"{motor_pv}.RBV")
    target = current + delta
    _caput(context, f"{motor_pv}.VAL", target, wait=False)


def wait_motors_done(context: Context, motor_x: str, motor_y: str, timeout: float = 10.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        dx = _caget(context, f"{motor_x}.DMOV")
        dy = _caget(context, f"{motor_y}.DMOV")
        if dx == 1 and dy == 1:
            return
        time.sleep(0.1)
    log.warning("motor move timeout")


# ── main ────────────────────────────────────────────────────────────

def main() -> int:
    logging.basicConfig(
        level=os.environ.get("BEAM_CENTER_LOG_LEVEL", "INFO"),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Soft IOC – closed-loop beam centering on overlay 1",
    )
    parser.add_argument("--camera", required=True,
                        help="Camera PV prefix, e.g. LAB:SIM:CAM01")
    parser.add_argument("--motor-x", required=True,
                        help="X motor PV, e.g. LAB:SIM:HMIR")
    parser.add_argument("--motor-y", required=True,
                        help="Y motor PV, e.g. LAB:SIM:VMIR")
    parser.add_argument("--prefix", required=True,
                        help="Soft IOC PV prefix, e.g. LAB:SIM:BEAM_CENTER")
    parser.add_argument("--pvout", default="pvlist.txt",
                        help="Path of the file where soft IOC PVs are dumped")
    args = parser.parse_args()

    camera = args.camera.rstrip(":")
    motor_x = args.motor_x.rstrip(":")
    motor_y = args.motor_y.rstrip(":")
    ioc_prefix = args.prefix.rstrip(":")
    pva_context = Context("pva")

    # ── soft IOC records ────────────────────────────────────────────
    from softioc import softioc, builder, asyncio_dispatcher  # type: ignore

    builder.SetDeviceName(ioc_prefix)

    gain_x_rec = builder.aOut("gain_x", initial_value=0.01,
                              DRVL=-10, DRVH=10, PREC=4)
    gain_y_rec = builder.aOut("gain_y", initial_value=0.01,
                              DRVL=-10, DRVH=10, PREC=4)
    tol_rec    = builder.aOut("tolerance", initial_value=5.0,
                              DRVL=0.1, DRVH=1000, EGU="px", PREC=1)
    interval_rec = builder.aOut("interval", initial_value=1.0,
                                DRVL=0.1, DRVH=60, EGU="s", PREC=1)

    err_x_rec  = builder.aIn("errX", initial_value=0, EGU="px", PREC=1)
    err_y_rec  = builder.aIn("errY", initial_value=0, EGU="px", PREC=1)
    status_rec = builder.stringIn("status", initial_value="Idle")

    start_rec  = builder.boolOut("start", initial_value=False,
                                 ZNAM="Idle", ONAM="Start")
    stop_rec   = builder.boolOut("stop", initial_value=False,
                                 ZNAM="Idle", ONAM="Stop")

    # ── control loop ────────────────────────────────────────────────
    loop_active = threading.Event()
    loop_thread = None

    def centering_loop():
        status_rec.set("Running")
        log.info("centering loop started")
        try:
            ensure_centroid_enabled(pva_context, camera)
            while loop_active.is_set():
                try:
                    beam_cx, beam_cy = read_beam_centroid(pva_context, camera)
                    ovl_cx, ovl_cy = read_overlay_center(pva_context, camera)

                    ex = ovl_cx - beam_cx
                    ey = ovl_cy - beam_cy
                    err_x_rec.set(round(ex, 1))
                    err_y_rec.set(round(ey, 1))

                    tol = tol_rec.get()
                    if abs(ex) < tol and abs(ey) < tol:
                        status_rec.set("Converged")
                        log.info("converged  err=(%.1f, %.1f)", ex, ey)
                        break

                    gx = gain_x_rec.get()
                    gy = gain_y_rec.get()
                    dx = ex * gx
                    dy = ey * gy

                    log.info("err=(%.1f, %.1f) px  move=(%.4f, %.4f)", ex, ey, dx, dy)
                    status_rec.set("Moving  err=%.0f,%.0f" % (ex, ey))

                    move_motor(pva_context, motor_x, dx)
                    move_motor(pva_context, motor_y, dy)
                    wait_motors_done(pva_context, motor_x, motor_y)

                except Exception:
                    log.exception("centering step failed")
                    status_rec.set("Error")
                    break

                interval = max(0.1, interval_rec.get())
                # interruptible sleep
                for _ in range(int(interval * 10)):
                    if not loop_active.is_set():
                        break
                    time.sleep(0.1)
        finally:
            loop_active.clear()
            start_rec.set(False)
            if status_rec.get() != "Converged":
                status_rec.set("Stopped")
            log.info("centering loop ended")

    def command_loop():
        nonlocal loop_thread
        prev_start = False
        prev_stop = False
        while True:
            start_value = bool(start_rec.get())
            stop_value = bool(stop_rec.get())

            if start_value and not prev_start and not loop_active.is_set():
                loop_active.set()
                loop_thread = threading.Thread(target=centering_loop, daemon=True)
                loop_thread.start()

            if stop_value and not prev_stop:
                loop_active.clear()
                stop_rec.set(False)

            prev_start = start_value
            prev_stop = stop_value
            time.sleep(0.1)

    threading.Thread(target=command_loop, daemon=True).start()

    # ── start IOC ───────────────────────────────────────────────────
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)
    dump_pvs(softioc, args.pvout)

    log.info("beam_center IOC running  prefix=%s  camera=%s  motors=(%s, %s)",
             ioc_prefix, camera, motor_x, motor_y)
    softioc.interactive_ioc(globals())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
