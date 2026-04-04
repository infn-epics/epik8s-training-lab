/* This script sets the value of Device Selection combobox widget. Useful
   when the main OPI is opened with DEVICE='valid_default_device' macro.
   
   Without this script the OPI with a specified DEVICE macro would still
   work, but the combobox widget would be empty and the user perhaps
   slightly confused. This is purely for cosmetics, but it's nice to have. */

importPackage(org.csstudio.display.builder.runtime.script);
importPackage(org.epics.vtype);

var device_macro = widget.getMacrosOrProperties().getValue("DEVICE");

var pv = PVUtil.getString(pvs[0]);

var pvstr =  widget.getPropertyValue("pv_value").getValue();
//java.lang.System.out.println("DEBUG: widget pv_value == " + pvstr);

if ((pvstr == "" || pvstr == "0") && device_macro != null) {
	/* This sets the value of the widget, but not the PV associated with it. */
	widget.setPropertyValue("pv_value", VString.of(device_macro,
                                                       Alarm.disconnected(), Time.now()));
}
