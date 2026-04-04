from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.csstudio.display.builder.model import WidgetFactory
from java.io import FileReader
from org.yaml.snakeyaml import Yaml
import os

logger = ScriptUtil.getLogger()

wtemplate = ScriptUtil.findWidgetByName(widget, "element_template")

conffile = widget.getEffectiveMacros().getValue("CONFFILE")
iocfilter = widget.getEffectiveMacros().getValue("IOCNAME")  # optional: filter by IOC name

display_model = widget.getDisplayModel()
display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))

if conffile is None:
    ScriptUtil.showMessageDialog(widget, "## Please set CONFFILE macro to a correct YAML configuration file")
    exit()

confpath = display_path + "/" + conffile

if not os.path.exists(confpath):
    ScriptUtil.showMessageDialog(widget, "## Cannot find file \"" + confpath + "\"")
    exit()

yaml = Yaml()
data = yaml.load(FileReader(confpath))
epics_config = data.get("epicsConfiguration")
if epics_config is None:
    ScriptUtil.showMessageDialog(widget, "Cannot find 'epicsConfiguration' in \"" + confpath + "\"")
    exit()

iocs = epics_config.get("iocs")
if iocs is None:
    ScriptUtil.showMessageDialog(widget, "Cannot find iocs section")
    exit()

# Collect all day_accumulators from all (or filtered) IOCs
accumulators = []
for ioc in iocs:
    ioc_name = ioc.get("name", "")
    iocprefix = ioc.get("iocprefix", "")
    day_acc = ioc.get("day_accumulators")

    if day_acc is None:
        continue

    if iocfilter and iocfilter != "ALL" and iocfilter != ioc_name:
        continue

    for acc in day_acc:
        pvname_raw = acc.get("pvname", "")
        daypv_raw = acc.get("daypv", "")
        egu = acc.get("egu", "")
        prec = str(acc.get("prec", "6"))
        desc = acc.get("desc", "Daily accumulator")
        factor = str(acc.get("factor", "1.0"))
        offset = str(acc.get("offset", "0.0"))
        pvenable = acc.get("pvenable", "")
        scan = acc.get("scan", "1 second")

        pvname = iocprefix + ":" + pvname_raw
        daypv = iocprefix + ":" + daypv_raw

        accumulators.append({
            "P": iocprefix,
            "IOCNAME": ioc_name,
            "PVNAME": pvname,
            "DAYPV": daypv,
            "NAME": pvname_raw.replace(":Charge", "").replace(":INTEGRAL", ""),
            "EGU": egu,
            "PREC": prec,
            "DESC": desc,
            "FACTOR": factor,
            "OFFSET": offset,
            "PVENABLE": pvenable,
            "SCAN": scan
        })

print("LoadAccumulators] Found " + str(len(accumulators)) + " day accumulators")

# Remove existing dynamic children
children_prop = widget.runtimeChildren()
for child in list(children_prop.getValue()):
    if child.getPropertyValue("name").startswith("Instance_acc"):
        children_prop.removeChild(child)

# Layout
offset_y = 5
embedded_width = wtemplate.getPropertyValue("width")
embedded_height = wtemplate.getPropertyValue("height") + offset_y
bobitem = widget.getEffectiveMacros().getValue("BOBITEM")
if bobitem is None:
    bobitem = "accumulator_row.bob"

for i in range(len(accumulators)):
    x = 0
    y = i * embedded_height
    macros = accumulators[i]

    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget()
    embedded.setPropertyValue("name", "Instance_acc" + str(i))
    embedded.setPropertyValue("x", x)
    embedded.setPropertyValue("y", y)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in macros.items():
        embedded.getPropertyValue("macros").add(macro, str(value))
    embedded.setPropertyValue("file", bobitem)
    widget.runtimeChildren().addChild(embedded)
