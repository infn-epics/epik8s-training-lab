importPackage(org.csstudio.display.builder.runtime.script);

var path = PVUtil.getString(pvs[0]);
var tifftemplate = "%s%s%d.tif";

// Set file paths
pvs[1].setValue(path);

// Set filename templates
pvs[2].setValue(tifftemplate);
