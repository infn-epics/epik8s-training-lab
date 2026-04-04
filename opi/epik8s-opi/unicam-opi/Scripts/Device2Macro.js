importPackage(org.csstudio.display.builder.runtime.script);
importPackage(org.csstudio.display.builder.model.properties);

var pv = PVUtil.getString(pvs[0]);
var macros = widget.getEffectiveMacros();
var device_macro = macros.getValue("DEVICE");

/* Don't display "0" in Device header when OPI first opens */
if (pv == 0) {
    if (device_macro != null) {
        pv = device_macro;
    } else {
        pv = "";
    }
}

//java.lang.System.out.println("DEBUG: Device2Macro.jsi called DEVICE == " + pv);

widget.getParent().get().propMacros().getValue().add("DEVICE", pv);

