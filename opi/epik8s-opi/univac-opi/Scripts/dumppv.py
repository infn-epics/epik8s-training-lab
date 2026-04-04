from org.csstudio.display.builder.runtime.script import ScriptUtil
from javax.swing import JOptionPane
from java.awt.datatransfer import StringSelection
from java.awt import Toolkit

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
listpv=""
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
    listpv = listpv + device_prefix + ":" + name+":"+pvname + "\n"


clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
clipboard.setContents(StringSelection(listpv), None)

# Show dialog with title and copiable content
JOptionPane.showMessageDialog(None, listpv, "PV List copied to clipboard", JOptionPane.INFORMATION_MESSAGE)
