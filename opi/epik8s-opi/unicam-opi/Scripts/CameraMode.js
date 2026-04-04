importPackage(org.csstudio.display.builder.runtime.script);

var camera_mode = PVUtil.getString(pvs[0]);

var range_ulimit = 0;

/* Set intensity graph's maximum is set according
   to selected camera mode (8bit/16bit). */
if (camera_mode == "UInt8") {
	range_ulimit = 255;
} else if (camera_mode == "UInt16") {
	range_ulimit = 65535;
} else {
	ScriptUtil.showMessageDialog(null, "Warning", "Unknown camera mode selected: '" + camera_mode + "'");
}

/* Set intensity graph's maximum. Minimum is always
   zero, so no need to change that. */
widget.setPropertyValue("maximum", range_ulimit);
