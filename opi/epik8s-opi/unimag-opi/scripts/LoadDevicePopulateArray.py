from org.csstudio.display.builder.runtime.script import ScriptUtil,PVUtil
from org.csstudio.display.builder.model import WidgetFactory

import os
from java.lang import Exception


def createInstance(x, y,macros):
    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget();
    embedded.setPropertyValue("x", x)
    embedded.setPropertyValue("y", y)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in macros.items():
            embedded.getPropertyValue("macros").add(macro, value)

    embedded.setPropertyValue("file", "MagnetChannel.bob")
    return embedded

logger = ScriptUtil.getLogger()

display_model =  widget.getDisplayModel()
devices=[]
embedded_width = 800
embedded_height = 30
zone = PVUtil.getString(pvs[0])
magtype = PVUtil.getString(pvs[1])
maginfo = eval(PVUtil.getString(pvs[2]))
print ("ZONE:"+ zone+ " TYPE:"+magtype )

for key in maginfo:
    includezone=False
    includetype=False

    if maginfo[key]['Zone'] == zone or zone == "all":
        includezone=True
    if maginfo[key]['Type'] == magtype or magtype == "all":
        includetype=True   
    if includezone and includetype:
        print ("ZONE:"+ zone+ " TYPE:"+magtype + " include:"+key + " prefix:"+maginfo[key]['Prefix'])

        devices.append({'R': key,"P":maginfo[key]['Prefix']})
    
display = widget.getDisplayModel()
rows = 35
children = display.runtimeChildren()
for ch in children.getValue():
    children.removeChild(ch)

# while children.getValue().size() > 0:
#     children.removeChild(children.get(0))
    
for i in range(len(devices)):
    # x = (i / rows) * embedded_width
    # y = 170 + embedded_height*(i % rows)
    x=0
    y= i * embedded_height
    instance = createInstance(x, y, devices[i])
    display.runtimeChildren().addChild(instance)
    