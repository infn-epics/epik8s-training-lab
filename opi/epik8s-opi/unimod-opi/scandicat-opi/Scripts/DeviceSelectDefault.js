/* This script sets the value of Device Selection combobox widget. Useful
   when the main OPI is opened with DEVICE='valid_default_device' macro.
   
   Without this script the OPI with a specified DEVICE macro would still
   work, but the combobox widget would be empty and the user perhaps
   slightly confused. This is purely for cosmetics, but it's nice to have. */

importPackage(Packages.org.csstudio.opibuilder.scriptUtil);

var device_macro = widget.getMacroValue("DEVICE");
var pv = widget.getPV();

if (widget.getValue() == "" && device_macro != null) {
	/* This sets the value of the widget, but not the PV associated with it. */
	widget.setValue(device_macro);
	
	/* It's important to set the value of loc://device PV to the same value. Otherwise the
	   local PV can trigger a widget value update with it's default value, which is "0.0". */
	pv.setValue(device_macro);
}
