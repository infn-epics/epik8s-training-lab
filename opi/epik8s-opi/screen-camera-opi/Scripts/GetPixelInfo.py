from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil
import re
# Access the widget (the parent of this script)
# widget = display.getWidget("CameraImage")  # Replace with your widget's name
logger = ScriptUtil.getLogger();

# Read Cursor Info PV
info_str=PVUtil.getString(pvs[0]);
if info_str:
    # Use regex to extract Value, xi, yi
    match = re.search(r'Value:\s*([0-9.eE+-]+),\s*xi:\s*(\d+),\s*yi:\s*(\d+)', info_str)

    if match:
        value = float(match.group(1))
        xi = int(match.group(2))
        yi = int(match.group(3))

        output_str = "X: "+str(xi)+", Y: "+str(yi)+", Value: "+str(value);
    else:
        output_str = ""

    # Write output to widget property
    widget.setPropertyValue("text", output_str);
else:
    pass;


