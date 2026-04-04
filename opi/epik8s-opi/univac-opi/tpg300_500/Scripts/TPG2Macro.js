importPackage(Packages.org.csstudio.bobbuilder.scriptUtil);

var macroInput = DataUtil.createMacrosInput(true);
var TPG300DeviceName = PVUtil.getString(pvArray[0]);

macroInput.put("TPG3002Macro", TPG300DeviceName);
widgetController.setPropertyValue("macros", macroInput);