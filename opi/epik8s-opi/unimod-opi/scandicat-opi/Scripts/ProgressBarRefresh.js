importPackage(Packages.org.csstudio.opibuilder.scriptUtil);

var pv_hopr = PVUtil.getDouble(pvArray[0]);

widgetController.setPropertyValue("minimum", 0);
widgetController.setPropertyValue("maximum", pv_hopr);