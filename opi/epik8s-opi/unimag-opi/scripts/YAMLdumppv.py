from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.csstudio.display.builder.model import WidgetFactory

from javax.swing import JOptionPane
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection

from org.yaml.snakeyaml import Yaml
from java.io import FileReader, BufferedWriter, FileWriter

import os
from java.lang import Exception
logger = ScriptUtil.getLogger()

conffile = widget.getEffectiveMacros().getValue("CONFFILE")
zoneSelector = widget.getEffectiveMacros().getValue("ZONE")
typeSelector = widget.getEffectiveMacros().getValue("TYPE")
devgroup_widget=widget.getEffectiveMacros().getValue("GROUP")

wtemplate = ScriptUtil.findWidgetByName(widget, "element_template") ## name of the hidden template

if devgroup_widget == None:
    ScriptUtil.showMessageDialog(widget, "Must Specify group widget (i.e unicool,univac,unimag) \"" + confpath + "\" please set CONFFILE macro to a correct file")

if zoneSelector == None:
    zoneSelector = PVUtil.getString(ScriptUtil.getPVs(widget)[0])

if typeSelector == None:
    typeSelector = PVUtil.getInt(ScriptUtil.getPVs(widget)[1])
    
display_model = widget.getDisplayModel()

display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))

confpath = display_path + "/" + conffile

if not os.path.exists(confpath):
    ScriptUtil.showMessageDialog(widget, "Cannot find file \"" + confpath + "\" please set CONFFILE macro to a correct file")

print("LOADING YAML:" + confpath + " zoneSelector: \"" + zoneSelector + " typeSelector: \"" + str(typeSelector)+"\"")


yaml = Yaml()
data = yaml.load(FileReader(confpath))
epics_config = data.get("epicsConfiguration")
if epics_config is None:
    ScriptUtil.showMessageDialog(widget, "Cannot find 'epicsConfiguration' in \"" + confpath + "\"")

    print("No 'epicsConfiguration' found.")
    exit()


iocs = epics_config.get("iocs")
if iocs is None:
    ScriptUtil.showMessageDialog(widget, "Cannot find iocs section, please provide a valid values.yaml file")
    exit()
# Merge iocDefaults into each IOC so per-template fields (e.g. devtype, opi) are available
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
# Parse conf file

devarray = []
device_prefix = widget.getEffectiveMacros().getValue("P")
listpv=""
for ioc in iocs:
    ioc_name = ioc.get("name", "")
    iocprefix = ioc.get("iocprefix", device_prefix)
    devtype = ioc.get("devtype", "ALL")
    devgroup = ioc.get("devgroup", "")
    devfunc  = ioc.get("devfunc", "")
    opi  = ioc.get("opi", "")
    zones = ioc.get("zones", "ALL")
    iocroot=ioc.get("iocroot", "")

    #print("Checking IOC:", ioc_name, "iocprefix:", iocprefix, "devtype:", devtype)    
    if iocprefix and devgroup == devgroup_widget:
        devices = ioc.get("devices", [])
        for dev in devices:
            name = dev['name']
            prefix=iocprefix
            devtype=ioc.get("devtype", "ALL")
            devfunc  = ioc.get("devfunc", "")

            if 'opi' in dev:
                opi=dev['opi']
            if 'zones' in dev:
                zones=dev['zones']
            if 'name' in dev:
                iocroot=dev['name']
            if 'devfunc' in dev:
                devfunc=dev['devfunc']
            if 'alias' in dev:
                name=dev['alias']
            if 'prefix' in dev:
                prefix=dev['prefix']
            print("Add object "+str(dev))

            if zoneSelector and zoneSelector != "ALL" and zoneSelector not in zones:
                continue
            if typeSelector and typeSelector != "ALL" and typeSelector != devfunc:
                continue
            if len(zones)==1:
                zone=zones[0]
            else:
                zone=str(zones)
                
            listpv = listpv + prefix + ":" + iocroot+":TEMP_RB\n"
            listpv = listpv + prefix + ":" + iocroot+":TEMP_SP\n"






clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
clipboard.setContents(StringSelection(listpv), None)

# Show dialog with title and copiable content
JOptionPane.showMessageDialog(None, listpv, "PV List copied to clipboard", JOptionPane.INFORMATION_MESSAGE)
