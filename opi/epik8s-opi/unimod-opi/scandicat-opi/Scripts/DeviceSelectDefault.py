# This script sets the value of Device Selection combobox widget. Useful
# when the main OPI is opened with DEVICE='valid_default_device' macro.
#   
# Without this script the OPI with a specified DEVICE macro would still
# work, but the combobox widget would be empty and the user perhaps
# slightly confused. This is purely for cosmetics, but it's nice to have. */

from org.csstudio.display.builder.runtime.script import ConsoleUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil

device_macro = widget.getEffectiveMacros().getValue("DEVICE")
writable = False
pval = ""

try:
    writable = widget.getPropertyValue("pv_writable")
    pname = widget.getPropertyValue("pv_name")
    # Remove type spec and what follows
    pname = pname[:pname.find('<')]
    pv = ScriptUtil.getPVByName(widget, pname)
    pval = pv.getValue()
except Exception as e:
    msgout = "Exception in DeviceSelectDefault.py " + str(e)
    ConsoleUtil.writeInfo(msgout)

if (writable and (len(pval) <= 0) and (device_macro is not None)):
    widget.setPropertyValue("pv_value", device_macro)
    pv.setValue(device_macro)
