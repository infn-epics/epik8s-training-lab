from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil

logger = ScriptUtil.getLogger()
pv = PVUtil.getString(pvs[0])
if pv and pv != "":

    device_list = epik8sutil.conf_to_dev(widget)

    device_actual = widget.getEffectiveMacros().getValue("DEVICE")
    logger.info("SELECTION:"+pv)
    for dev in device_list:
        if pv == dev["NAME"]:
            logger.info("Found device: " + str(dev))
            widget.setPropertyValue("file","")
            widget.getPropertyValue("macros").add("DEVICE", dev["P"])
            widget.getPropertyValue("macros").add("HW", dev["TYPE"])
            widget.getPropertyValue("macros").add("CAM", dev["R"])
            widget.setPropertyValue("file","Camera_Main.bob")


