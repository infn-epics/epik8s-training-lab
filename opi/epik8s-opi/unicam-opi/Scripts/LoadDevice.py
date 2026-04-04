from org.csstudio.display.builder.runtime.script import ScriptUtil,PVUtil
#from org.csstudio.display.builder.runtime import ActionUtil
import os
from java.lang import Exception
import epik8sutil
logger = ScriptUtil.getLogger()

# axis = ScriptUtil.findWidgetByName(widget, "TML_AXIS")
combo = ScriptUtil.findWidgetByName(widget, "DeviceCombo")
# Initialize an empty list to store the values
device_list = epik8sutil.conf_to_dev(widget)
print ("Device list: " + str(device_list))
names= []
for dev in device_list:
    if "NAME" in dev:
        names.append(dev["NAME"])
    else:
        logger.error("Device configuration missing 'name' field: " + str(dev))

combo.setItems(names)

if len(device_list):  ## put the first as default if nothing selected yet
    current = PVUtil.getString(pvs[0])
    if not current or current == "":
        ScriptUtil.getPrimaryPV(combo).write(names[0])



