importPackage(Packages.org.csstudio.opibuilder.scriptUtil);

var macroInput = DataUtil.createMacrosInput(true);
var pv = PVUtil.getString(pvArray[0]);
var device_macro = widget.getMacroValue("DEVICE");

/* Don't display "0.0" in Device header when OPI first opens */
if (pv == 0.0) {
    if (device_macro != null) {
        pv = device_macro;
    } else {
        pv = "";
    }
}

macroInput.put("DEVICE", pv);
widgetController.setPropertyValue("macros", macroInput);
