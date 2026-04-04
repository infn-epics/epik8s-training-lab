from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.csstudio.display.builder.model import WidgetFactory

import os
from java.lang import Exception

def csv_to_list(csv_file):
    result = []

    with open(csv_file, 'r') as file:
        # Read lines from the file
        lines = file.readlines()
        # Extract the header
        header = [col.strip() for col in lines[0].split(",")]
        # Process each row
        for line in lines[1:]:
            values = [value.strip() for value in line.split(",")]
            row_dict = dict(zip(header, values))
            result.append(row_dict)
    return result

logger = ScriptUtil.getLogger()

conffile = widget.getEffectiveMacros().getValue("CONFFILE")
zoneSelector = widget.getEffectiveMacros().getValue("ZONE")
typeSelector = widget.getEffectiveMacros().getValue("TYPE")
wtemplate = ScriptUtil.findWidgetByName(widget, "element_template") ## name of the hidden template

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
    pvname="PRES_RB"
    name=device['Name']
    opipath=""
    if not 'Zone' in device:
        continue
    zones = device['Zone'].split(';')
    if zoneSelector and zoneSelector != "ALL" and zoneSelector not in zones:
        continue
    
    if typeSelector and int(typeSelector) != -1 and (not ('Type' in device) or typeSelector != device['Type']):
        continue
    if 'PvName' in device:
        pvname = device['PvName']
    if 'Alias' in device:
        name = device['Alias']
    
    if 'Prefix' in device:
        device_prefix = device['Prefix']

    if 'Opi' in device:
        opipath = device['Opi']
    devices.append({'NAME':name,'R': device['Name'], "P": device_prefix, "TYPE": device['Type'], "ZONE": device['Zone'],"PVNAME":pvname,"OPI":opipath})
    logger.info("loading " + device['Name'])

offset = 5
embedded_width  = wtemplate.getPropertyValue("width")
embedded_height = wtemplate.getPropertyValue("height") + offset

def createInstance(x, y, macros):
    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget()
    embedded.setPropertyValue("x", x)
    embedded.setPropertyValue("y", y)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in macros.items():
        embedded.getPropertyValue("macros").add(macro, value)

    embedded.setPropertyValue("file", "VacuumChannel.bob")
    return embedded

display = widget.getDisplayModel()
rows = 35
for i in range(len(devices)):
    x = 0
    y = i * embedded_height
    instance = createInstance(x, y, devices[i])
    widget.runtimeChildren().addChild(instance)