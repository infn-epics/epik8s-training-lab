#!/usr/bin/env python3
"""
Soft IOC that generates random overlay positions on a camera.

Exposes PVs under a configurable prefix:
  - maxx, maxy   : max random offset in pixels (default 200)
  - size          : overlay width/height in pixels (default 50)
  - X, Y          : center position in pixels (default 500, 500)
  - run           : 0/1 toggle – when set to 1, generates a random offset,
                    writes the overlay rectangle, then resets to 0

When *run* transitions to 1 the IOC:
  1. draws two uniform random numbers  dx in [-maxx, +maxx], dy in [-maxy, +maxy]
  2. computes overlay center = (X + dx, Y + dy)
  3. sets Overlay1:1:PositionX/Y  and  SizeX/Y  on the target camera
  4. enables Overlay1:EnableCallbacks and Overlay1:1:Use
"""
import argparse
import logging
import os
import random
import time

import epics  # pyepics – CA put/get


log = logging.getLogger("overlay_rnd")


def apply_overlay(camera_prefix: str, cx: int, cy: int, w: int, h: int) -> None:
    """Write rectangle geometry to overlay slot 1 of the target camera."""
    base = f"{camera_prefix}:Overlay1"

    epics.caput(f"{base}:EnableCallbacks", 1, wait=True, timeout=2.0)
    epics.caput(f"{base}:1:Use", 1, wait=True, timeout=2.0)
    epics.caput(f"{base}:1:Shape", 1, wait=True, timeout=2.0)

    # PositionX/Y are the top-left corner; convert from center
    pos_x = max(0, cx - w // 2)
    pos_y = max(0, cy - h // 2)

    epics.caput(f"{base}:1:PositionX", pos_x, wait=True, timeout=2.0)
    epics.caput(f"{base}:1:PositionY", pos_y, wait=True, timeout=2.0)
    epics.caput(f"{base}:1:SizeX", w, wait=True, timeout=2.0)
    epics.caput(f"{base}:1:SizeY", h, wait=True, timeout=2.0)

    log.info("overlay set  center=(%d,%d)  pos=(%d,%d)  size=(%dx%d)",
             cx, cy, pos_x, pos_y, w, h)


def main() -> int:
    logging.basicConfig(
        level=os.environ.get("OVERLAY_RND_LOG_LEVEL", "INFO"),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Soft IOC – random overlay rectangle on a camera",
    )
    parser.add_argument("--camera", required=True,
                        help="Camera PV prefix, e.g. LAB:SIM:CAM01")
    parser.add_argument("--prefix", required=True,
                        help="Prefix for the soft IOC PVs, e.g. LAB:SIM:OVERLAY_RND")
    args = parser.parse_args()

    camera_prefix = args.camera.rstrip(":")
    ioc_prefix = args.prefix.rstrip(":")

    # ── soft IOC setup ──────────────────────────────────────────────
    from softioc import softioc, builder, asyncio_dispatcher  # type: ignore

    builder.SetDeviceName(ioc_prefix)

    maxx_rec = builder.aOut("maxx", initial_value=200,
                            DRVL=0, DRVH=5000, EGU="px")
    maxy_rec = builder.aOut("maxy", initial_value=200,
                            DRVL=0, DRVH=5000, EGU="px")
    size_rec = builder.aOut("size", initial_value=50,
                            DRVL=1, DRVH=5000, EGU="px")
    x_rec    = builder.aOut("X", initial_value=500,
                            DRVL=0, DRVH=10000, EGU="px")
    y_rec    = builder.aOut("Y", initial_value=500,
                            DRVL=0, DRVH=10000, EGU="px")
    run_rec  = builder.boolOut("run", initial_value=False,
                               ZNAM="Idle", ONAM="Go")

    out_cx   = builder.aIn("outX", initial_value=0, EGU="px")
    out_cy   = builder.aIn("outY", initial_value=0, EGU="px")

    def on_run(value):
        if not value:
            return
        try:
            mx = int(maxx_rec.get())
            my = int(maxy_rec.get())
            sz = int(size_rec.get())
            bx = int(x_rec.get())
            by = int(y_rec.get())

            dx = random.randint(-mx, mx)
            dy = random.randint(-my, my)
            cx = bx + dx
            cy = by + dy

            out_cx.set(cx)
            out_cy.set(cy)

            apply_overlay(camera_prefix, cx, cy, sz, sz)
        except Exception:
            log.exception("overlay generation failed")
        finally:
            run_rec.set(False)

    run_rec.add_callback(on_run)

    # ── start IOC ───────────────────────────────────────────────────
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)

    log.info("overlay_rnd IOC running  prefix=%s  camera=%s", ioc_prefix, camera_prefix)
    softioc.interactive_ioc(globals())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
