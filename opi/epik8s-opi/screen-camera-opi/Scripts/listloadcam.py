#By default, Phoebus uses Jython for scripting (accessible from the Script or Python panels).
#To use the YAML functionality in Phoebus --> use Java’s SnakeYAML in Jython
from org.yaml.snakeyaml import Yaml
from java.io import FileReader, BufferedWriter, FileWriter
from java.util import ArrayList

from org.csstudio.display.builder.runtime.script import ScriptUtil,PVUtil
import os

conffile = widget.getEffectiveMacros().getValue("CONFFILE")
display_model = widget.getDisplayModel()
display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))

if conffile is None:
    ScriptUtil.showMessageDialog(widget, "## Please set CONFFILE macro to a correct YAML configuration file")
    exit()    
    
yaml_file = display_path + "/" + conffile    

if not os.path.isfile(yaml_file):
    ScriptUtil.showMessageDialog(widget, "## "+yaml_file+" does not  exists: please set CONFFILE macro to a correct YAML configuration file")
    exit()    

print("Loading file '%s'." % yaml_file)

# Load YAML file using SnakeYAML
yaml = Yaml()
data = yaml.load(FileReader(yaml_file))
#print("Top-level keys:", data.keySet())

# Get epicsConfiguration -> iocs list
epics_config = data.get("epicsConfiguration")
if epics_config is None:
    print("No 'epicsConfiguration' found.")
    exit()

iocs = epics_config.get("iocs")
if iocs is None:
    print("No 'iocs' section found.")
    exit()

# Merge iocDefaults into each IOC so per-template fields (e.g. devtype) are available
ioc_defaults = data.get("iocDefaults")
if ioc_defaults:
    merged_iocs = []
    for ioc in iocs:
        tmpl = ioc.get("template") or ioc.get("devtype") or ""
        tmpl_defaults = ioc_defaults.get(tmpl)
        if tmpl_defaults:
            merged = dict(tmpl_defaults)
            merged.update(dict(ioc))
            merged_iocs.append(merged)
        else:
            merged_iocs.append(ioc)
    iocs = merged_iocs

# Find cameras under IOCs with iocprefix ":CAM" and devtype "camera"
device_list=[]
for ioc in iocs:
    ioc_name = ioc.get("name", "")
    iocprefix = ioc.get("iocprefix", "")
    devtype = ioc.get("devtype", "")
    #get the widget macros
    #ioc_prefname=widget.getEffectiveMacros().getValue("DEVICE")
    #ioc_devtype=widget.getEffectiveMacros().getValue("DEVTYPE")  
    #if iocprefix and iocprefix.endswith(ioc_prefname) and devtype == ioc_devtype:
    if iocprefix and "camera" in devtype :
        cameras = ioc.get("devices", [])
        if cameras:
            for cam in cameras:
                cam_name = cam.get("name", "")
                if cam_name:
                    #results.add((cam_name, ioc_name))
                    out_str=cam_name+" ("+ioc_name+")"
                    device_list.append(out_str)
                    print("Found: "+out_str)

# Sort results by camera name
device_list.sort()
print("Total devices found: "+str(len(device_list)))

#####################################
# put the list in the cam menu box ##
#####################################
combo = ScriptUtil.findWidgetByName(widget,"CamMenu")
combo.setItems(device_list)
if len(device_list): #remove the first item (pv initialization)
    ScriptUtil.getPrimaryPV(combo).write(device_list[0])
print("Cam menu updated!")

