from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.phoebus.pv import PVPool

def set_current_selected():
    """Set current for all selected magnets"""
    # Get the current value from the text entry widget
    current_widget = ScriptUtil.findWidgetByName(widget.getDisplayModel(), "entryCurrent")
    if current_widget is None:
        ScriptUtil.showMessageDialog(widget, "Error: Could not find current entry widget")
        return
    
    current_pv = ScriptUtil.getPrimaryPV(current_widget)
    current_value = PVUtil.getDouble(current_pv)
    
    if current_value is None:
        ScriptUtil.showMessageDialog(widget, "Error: Please enter a valid current value")
        return
    
    lpvs = PVPool.getPVReferences()
    count = 0
    errors = []
    
    for pvr in lpvs:
        selection_pv = pvr.getEntry()
        name = selection_pv.getName()
        
        if name.startswith("loc://selection:"):
            if selection_pv.read().getValue() == 1:
                pv_prefix = name.replace("loc://selection:", "")
                prefix, identifier = pv_prefix.rsplit(":", 1)
                
                try:
                    # Set current setpoint for the magnet
                    current_sp_pv = PVUtil.createPV(pv_prefix + ":CURRENT_SP", 100)
                    current_sp_pv.write(current_value)
                    count += 1
                    print("Set current "+str(current_value)+" A for magnet: "+identifier)
                    
                except Exception as e:
                    error_msg = "Error setting current for "+identifier+": "+str(e)
                    errors.append(error_msg)
                    print(error_msg)
    
    # Show result message
    if errors:
        error_text = "\n".join(errors)
        ScriptUtil.showMessageDialog(widget, "Set current for "+str(count)+" magnets to "+str(current_value)+"A\n\nErrors:\n"+error_text)
    else:
        ScriptUtil.showMessageDialog(widget, "Successfully set current to "+str(current_value)+"A for "+str(count)+" selected magnets")

# Execute the function
set_current_selected()