importPackage(org.csstudio.display.builder.runtime.script);
importPackage(org.csstudio.display.builder.model.properties);

var fakeColor = Boolean( Number( PVUtil.getLong(pvs[0]) ) );

if (fakeColor == true) {
	widget.setPropertyValue("color_map", PredefinedColorMaps.SPECTRUM);
	}

if (fakeColor == false) {
	widget.setPropertyValue("color_map", PredefinedColorMaps.GRAY);
	}
