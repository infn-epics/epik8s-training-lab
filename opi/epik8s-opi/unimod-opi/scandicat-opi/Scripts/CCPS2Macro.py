from org.csstudio.opibuilder.scriptUtil import DataUtil, PVUtil
from org.csstudio.display.builder.runtime.script import ConsoleUtil
from org.phoebus.framework.macros import Macros

# Crea un oggetto per l'input delle macro
macro_input = DataUtil.createMacrosInput(True)



# Ottieni il valore del PV
pv = PVUtil.getString(pvs[0])

# L'indice CCPS è l'ultimo carattere della stringa
ccps_index = pv[-1]

mkeyset = widget.getEffectiveMacros().getNames()
newmacros = Macros()
for mkey in mkeyset:
    if (mkey == "CCPS_NUM"):
        continue

    mval = widget.getEffectiveMacros().getValue(mkey)
    newmacros.add(mkey, mval)

newmacros.add("CCPS_NUM", ccps_index)

try:
   widget.setPropertyValue("macros", newmacros)
   #widget.setPropertyValue("file", "")
   #widget.setPropertyValue("file", "ScandinovaRFMod_CCPSStatus.bob")
except Exception as ex:
   mmmex = "Device2Macro: Exception caught: " + str(ex)
   ConsoleUtil.writeInfo(mmmex)
