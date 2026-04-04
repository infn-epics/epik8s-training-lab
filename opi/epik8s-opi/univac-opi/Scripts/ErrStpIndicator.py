from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil
from org.csstudio.display.builder.model.properties import WidgetColor

#Get info from macros
prefx = widget.getEffectiveMacros().getValue("P")
mydev = widget.getEffectiveMacros().getValue("R")

if 'VGA' in mydev:
    pvName=PVUtil.createPV(prefx+":ERROR",100)
    pv_value=PVUtil.getString(pvName)
    if 'No error' in pv_value:
        pv_value="OK"
    else:
        pv_value="NOK"
else:
    pvName1=PVUtil.createPV(prefx+":"+mydev+":STPTSTAT_RB",100)
    pv_value1=PVUtil.getString(pvName1)
    pvName2=PVUtil.createPV(prefx+":"+mydev+":STATUS_RB",100)
    pv_value2=PVUtil.getString(pvName2)
    if 'ON' in pv_value1 and 'ON' in pv_value2:
        pv_value="OK"
    else:
        pv_value="NOK"

widget.setPropertyValue('text',pv_value)
if 'NOK' in pv_value:
    widget.setPropertyValue("background_color", WidgetColor(255, 0, 0)) #red
else:
    widget.setPropertyValue("background_color", WidgetColor(0, 255, 0)) #green
