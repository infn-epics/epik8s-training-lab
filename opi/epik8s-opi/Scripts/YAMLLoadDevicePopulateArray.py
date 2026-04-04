from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil

import epik8sutil

import os
from java.lang import Exception
logger = ScriptUtil.getLogger()

# zoneSelector = widget.getEffectiveMacros().getValue("ZONE")
# typeSelector = widget.getEffectiveMacros().getValue("TYPE")
# devgroup_widget=widget.getEffectiveMacros().getValue("GROUP")
wtemplate = ScriptUtil.findWidgetByName(widget, "element_template") ## name of the hidden template
# conffile = widget.getEffectiveMacros().getValue("CONFFILE")
# display_model = widget.getDisplayModel()
# display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))

# if conffile is None:
#     ScriptUtil.showMessageDialog(widget, "## Please set CONFFILE macro to a correct YAML configuration file")
#     exit()
# confpath = display_path + "/" + conffile

devarray = []
devarray = epik8sutil.conf_to_dev(widget)

offset = 5
embedded_width  = wtemplate.getPropertyValue("width")
embedded_height = wtemplate.getPropertyValue("height") + offset
devgroup_widget=widget.getEffectiveMacros().getValue("GROUP")
bobitem=widget.getEffectiveMacros().getValue("BOBITEM")
if bobitem is None:
   bobitem=devgroup_widget+ "_channel.bob"
display = widget.getDisplayModel()
# Remove all existing runtime children first
children_prop = widget.runtimeChildren()
for child in list(children_prop.getValue()):
    if child.getPropertyValue("name").startswith("Instance_" + devgroup_widget):
        children_prop.removeChild(child)


for i in range(len(devarray)):
    x = 0
    y = i * embedded_height
    instance = epik8sutil.createInstance(embedded_width,embedded_height,devgroup_widget+str(i),bobitem,x, y, devarray[i])
    widget.runtimeChildren().addChild(instance)