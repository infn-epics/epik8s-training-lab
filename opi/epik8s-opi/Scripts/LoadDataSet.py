from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
import epik8sutil

name = PVUtil.getString(pvs[0])

# pv = ScriptUtil.getPrimaryPV(filename)
# name = PVUtil.getString(pv)
print "Loading: "+name
#dataset =  ScriptUtil.findWidgetByName(widget, "DataSet")
#loadset = ScriptUtil.findWidgetByName(widget, "LoadSetting")
#loadset.setPropertyValue("enabled",False)
epik8sutil.load_pv_fromfile(widget,name)

