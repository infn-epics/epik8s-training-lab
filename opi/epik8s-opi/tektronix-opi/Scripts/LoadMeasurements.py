from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.csstudio.display.builder.model import WidgetFactory
from java.io import FileReader
from org.yaml.snakeyaml import Yaml
import os

logger = ScriptUtil.getLogger()

wtemplate = ScriptUtil.findWidgetByName(widget, "element_template")

conffile = widget.getEffectiveMacros().getValue("CONFFILE")
iocfilter = widget.getEffectiveMacros().getValue("IOCNAME")  # name of the IOC to load

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

# Collect measurement devices from the matching IOC
measurements = []
for ioc in iocs:
    ioc_name = ioc.get("name", "")
    iocprefix = ioc.get("iocprefix", "")
    devices = ioc.get("devices")

    if devices is None:
        continue

    if iocfilter and iocfilter != "ALL" and iocfilter != ioc_name:
        continue

    for dev in devices:
        devtype = dev.get("devtype", "")
        if devtype != "measurement":
            continue

        channel = dev.get("channel", 0)
        name = dev.get("name", "CH%d" % channel)
        coeff = str(dev.get("coeff", "1"))
        enablepv = dev.get("enablepv", "")

        measurements.append({
            "P": iocprefix,
            "IOCNAME": ioc_name,
            "MEAS": str(channel),
            "NAME": name,
            "COEFF": coeff,
            "ENABLEPV": enablepv,
        })

logger.info("LoadMeasurements: Found " + str(len(measurements)) + " measurement devices")

# Remove existing dynamic children
children_prop = widget.runtimeChildren()
for child in list(children_prop.getValue()):
    if child.getPropertyValue("name").startswith("Instance_meas"):
        children_prop.removeChild(child)

# Layout
offset_y = 5
embedded_width = wtemplate.getPropertyValue("width")
embedded_height = wtemplate.getPropertyValue("height") + offset_y
bobitem = widget.getEffectiveMacros().getValue("BOBITEM")
if bobitem is None:
    bobitem = "meas_asyn_row.bob"

for i, meas in enumerate(measurements):
    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget()
    embedded.setPropertyValue("name", "Instance_meas" + str(i))
    embedded.setPropertyValue("x", 0)
    embedded.setPropertyValue("y", i * embedded_height)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in meas.items():
        embedded.getPropertyValue("macros").add(macro, str(value))
    embedded.setPropertyValue("file", bobitem)
    widget.runtimeChildren().addChild(embedded)
