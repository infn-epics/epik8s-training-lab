from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.csstudio.display.builder.model import WidgetFactory
from confutil import csv_to_list
import os
from java.lang import Exception


logger = ScriptUtil.getLogger()

conffile = widget.getEffectiveMacros().getValue("CONFFILE")
zoneSelector = widget.getEffectiveMacros().getValue("ZONE")
typeSelector = widget.getEffectiveMacros().getValue("TYPE")
name= widget.getEffectiveMacros().getValue("TEMPLATE")
if name == None:
    name = "MagnetChannel.bob"

wtemplate = ScriptUtil.findWidgetByName(widget, "element_template") ## name of the hidden template

if wtemplate == None:
    ScriptUtil.showMessageDialog(widget, "Cannot find hidden template widget named \"element_template\" in "+name)

if zoneSelector == None:
    zoneSelector = PVUtil.getString(ScriptUtil.getPVs(widget)[0])

if typeSelector == None:
    typeSelector = PVUtil.getInt(ScriptUtil.getPVs(widget)[1])
    
display_model = widget.getDisplayModel()

display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))

confpath = display_path + "/" + conffile

if not os.path.exists(confpath):
    ScriptUtil.showMessageDialog(widget, "Cannot find file \"" + confpath + "\" please set CONFFILE macro to a correct file")

# Parse conf file
print("LOADING:" + confpath + " zoneSelector: \"" + zoneSelector + " typeSelector: \"" + str(typeSelector)+"\"")

devinfo = csv_to_list(confpath)

# Initialize an empty list to store the values
devices = []
device_prefix = widget.getEffectiveMacros().getValue("P")

# Process each device
for device in devinfo:
    # logger.info("device " + device['Name'] + " zone " + device['Zone'] + " type " + device['Type'])
    opi=""
    if 'Prefix' in device:
        device_prefix = device['Prefix']
    
    ## device['Zone'] may contain multiple zones separated by comma
    if not 'Zone' in device:
        continue
    zones = device['Zone'].split(';')
    if zoneSelector and zoneSelector != "ALL" and zoneSelector not in zones:
        continue
    if typeSelector and typeSelector != "ALL" and typeSelector != device['Type']:
        continue
    
    if 'OPI' in device:
        opi = device['OPI']
        
    devices.append({'R': device['Name'], "P": device_prefix, "TYPE": device['Type'], "ZONE": device['Zone'],"OPI": opi})
    logger.info("loading " + device['Name'])


embedded_width_margin  = 0
embedded_height_margin = 0
embedded_width  = wtemplate.getPropertyValue("width")
embedded_height = wtemplate.getPropertyValue("height")

def createInstance(x, y,macros,name):
    
    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget();
    embedded.setPropertyValue("x", x)
    embedded.setPropertyValue("y", y)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in macros.items():
            embedded.getPropertyValue("macros").add(macro, value)

    embedded.setPropertyValue("file", name)
    return embedded

rows = 35
for i in range(len(devices)):
    # x = (i / rows) * embedded_width
    # y = 170 + embedded_height*(i % rows)
    x=embedded_width_margin
    y= i * (embedded_height+embedded_height_margin)
    instance = createInstance(x, y, devices[i],name)
    widget.runtimeChildren().addChild(instance)
