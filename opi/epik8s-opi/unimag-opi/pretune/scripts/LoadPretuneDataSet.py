from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from confutil import csv_to_list
from org.csstudio.display.builder.model import WidgetFactory
import os
def createInstance(x, y,macros):
    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget()
    embedded.setPropertyValue("name", "item-"+str(y/embedded_height))

    embedded.setPropertyValue("x", x)
    embedded.setPropertyValue("y", y)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in macros.items():
            embedded.getPropertyValue("macros").add(macro, value)

    embedded.setPropertyValue("file", "pretune-ele.bob")
    return embedded

# logger = ScriptUtil.getLogger()
device_prefix = widget.getEffectiveMacros().getValue("P")

# logger.info("device " +device_prefix )
if not device_prefix:
    device_prefix="NOPREFIX"

name = PVUtil.getString(pvs[0])


# pv = ScriptUtil.getPrimaryPV(filename)
# name = PVUtil.getString(pv)
print "Loading: "+name
#dataset =  ScriptUtil.findWidgetByName(widget, "DataSet")
#loadset = ScriptUtil.findWidgetByName(widget, "LoadSetting")
#loadset.setPropertyValue("enabled",False)

wtemplate = ScriptUtil.findWidgetByName(widget, "element_template") ## name of the hidden template

interlinea=5

embedded_width  = wtemplate.getPropertyValue("width")
embedded_height = wtemplate.getPropertyValue("height") +interlinea
offy=0
cnt=0

if name:
    ## new syntax Name, Prefix, Current, State
    devinfo = csv_to_list(name)
    for d in devinfo:
        x=0
        y= offy+ cnt * (embedded_height)
        
        prefix=d['Prefix']
        identifier=d['Name']
        m={'R': identifier,'P': prefix}
        print("ELE "+str(d))
        instance = createInstance(x, y, m)
        widget.runtimeChildren().addChild(instance)
        loc_current = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":current",10)
        loc_state = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":state",10)
        loc_current.write(d['Current'])
        loc_state.write(d['State'])

        # if d['State']=="ON":
        #     loc_state.write(1)
        # else:
        #     loc_state.write(2)

        cnt=cnt+1
        
    