from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ConsoleUtil
from org.phoebus.framework.macros import Macros

pv = PVUtil.getString(pvs[0])
device_macro = widget.getEffectiveMacros().getValue("DEVICE")

# Don't display "0.0" in Device header when OPI first opens 
if (pv == "0.0"): 
    if (device_macro is not None):
        pv = device_macro;
    else:
        pv = ""

#message = "DEBUG: Setting DEVICE==" + pv + " to widget named " + widget.getName()
#ConsoleUtil.writeInfo(message)

mkeyset = widget.getEffectiveMacros().getNames()
newmacros = Macros()
for mkey in mkeyset:
    if (mkey == "DEVICE"):
        continue

    mval = widget.getEffectiveMacros().getValue(mkey)
    newmacros.add(mkey, mval)

newmacros.add("DEVICE", pv)

try:
   widget.setPropertyValue("macros", newmacros)
   widget.setPropertyValue("file", "")
   widget.setPropertyValue("file", "TML_Main.bob")
except Exception as ex:
   mmmex = "Device2Macro: Exception caught: " + str(ex)
   ConsoleUtil.writeInfo(mmmex)

