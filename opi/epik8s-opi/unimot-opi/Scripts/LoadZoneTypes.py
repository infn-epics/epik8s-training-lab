from org.csstudio.display.builder.runtime.script import ScriptUtil,PVUtil
import os
from java.lang import Exception
import epik8sutil

print(widget.getName() + "] Starting LoadZoneTypes.py")

devarray = epik8sutil.conf_to_dev(widget)
zones_set = set()
type_set = set()
func_set = set()
if not devarray:
    group = widget.getEffectiveMacros().getValue("GROUP")
    if group is None:
        group = "mag"
    ScriptUtil.showMessageDialog(widget, "No devices found for group: " + group)
else:
    combozone = ScriptUtil.findWidgetByName(widget, "Zonecombo")
    combofunc = ScriptUtil.findWidgetByName(widget, "Funccombo")
    combotype = ScriptUtil.findWidgetByName(widget, "Typecombo")

    # Find the combo box widget
  
    if combozone is None:
        ScriptUtil.showMessageDialog(widget, "Cannot find Zonecombo widget")
    elif combofunc is None:
        ScriptUtil.showMessageDialog(widget, "Cannot find Funccombo widget")

    else:
        # Build device list from devarray
        device_list = []
        print(widget.getName() + "] FOUND " + str(len(devarray)) + " devices in configuration file")
        zones_set.add("ALL")
        func_set.add("ALL")
        type_set.add("ALL")
        
        for dev in devarray:
            # Use the device name
            
            funcdev=dev.get('FUNC','')
            zoneadd = dev.get('ZONE', '')
            typedev=dev.get('TYPE','')
            if zoneadd:
                zones_set.add(zoneadd)

            if funcdev:
                func_set.add(funcdev)

            if typedev:
                type_set.add(typedev)

        
        combozone.setItems(list(zones_set))
        combofunc.setItems(list(func_set))
        combotype.setItems(list(type_set))

