from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
logger = ScriptUtil.getLogger()
x_value_to_name = {
    2.0: "bpm0",
    2.5: "bpm1",
    3.0: "bpm2",
    3.5: "bpm4"
    # Add other mappings as needed
}

def main():
    xy_plot_widget = ScriptUtil.findWidgetByName(widget, 'aggregator_graph')
    x_value=0
    # Check if the widget was found
    if xy_plot_widget is not None:
        # Retrieve the X value of the first trace (example usage)
        x_pv_name = xy_plot_widget.getPropertyValue('traces[0].x_pv')
        logger.info("x_pv_name: "+ x_pv_name)
        #print (PVUtil.getDouble(x_pv_name))
        for i in ScriptUtil.getPVs(widget):
            #logger.info("name: "+ str(i)+ " val ="+str(PVUtil.getDouble(i)))
           
            if (str(i) == x_pv_name):
                x_value=PVUtil.getDouble(i)
                print("TROVATO")
                break
        #x_pv_value=
        #x_pv_value = PVUtil.getDouble(ScriptUtil.getPV(x_pv_name))
        
        # Find the corresponding name for the X value
        x_name = x_value_to_name.get(x_value, str(x_value))
        
        # Set the tooltip to show the name corresponding to the X value
        tooltip_text = x_name
        xy_plot_widget.setPropertyValue('tooltip', tooltip_text)
    else:
        print("X/Y Plot widget not found")
    
    return True

main()