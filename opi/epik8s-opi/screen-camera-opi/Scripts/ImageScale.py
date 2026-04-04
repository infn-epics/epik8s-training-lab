from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil
# Access the widget (the parent of this script)
# widget = display.getWidget("CameraImage")  # Replace with your widget's name
logger = ScriptUtil.getLogger();

# Get PV values (replace with your PV names)
min_value = 0 #PVUtil.getDouble(pvs[0])
max_value = PVUtil.getDouble(pvs[0]);

if max_value:
    # Set colormap range
    pass;
else:
	max_value=1000;

widget.setPropertyValue("minimum", min_value);
widget.setPropertyValue("maximum", max_value);

