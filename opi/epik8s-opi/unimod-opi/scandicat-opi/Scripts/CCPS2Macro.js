importPackage(Packages.org.csstudio.opibuilder.scriptUtil);

var macroInput = DataUtil.createMacrosInput(true);
var pv = PVUtil.getString(pvArray[0]);

/* CCPS index is the last character in the string */
ccps_index = pv.substr(pv.length() - 1, 1);

macroInput.put("CCPS_NUM", ccps_index);
widgetController.setPropertyValue("macros", macroInput);
