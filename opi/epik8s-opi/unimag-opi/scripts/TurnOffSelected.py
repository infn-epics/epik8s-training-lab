from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.phoebus.pv import PVPool

def turn_off_selected():
    """Turn OFF all selected magnets"""
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
                    # Turn OFF the magnet by setting state to OFF
                    state_sp_pv = PVUtil.createPV(pv_prefix + ":STATE_SP", 100)
                    state_sp_pv.write("OFF")
                    count += 1
                    print("Turned OFF magnet: "+identifier)
                    
                except Exception as e:
                    error_msg = "Error turning OFF "+identifier+": "+str(e)
                    errors.append(error_msg)
                    print(error_msg)
    
    # Show result message
    if errors:
        error_text = "\n".join(errors)
        ScriptUtil.showMessageDialog(widget, "Turned OFF "+str(count)+" magnets\n\nErrors:\n"+error_text)
    else:
        ScriptUtil.showMessageDialog(widget, "Successfully turned OFF "+str(count)+" selected magnets")

# Execute the function
turn_off_selected()