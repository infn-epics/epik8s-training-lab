from org.csstudio.opibuilder.scriptUtil import PVUtil, FileUtil, DataUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
import os
from java.lang import Exception

from PV2File import Deserializer
logger = ScriptUtil.getLogger()

def update_widgets(widget):
    widget.update()
    #for child in widget.children:
    #    update_widgets(child)


def main():
    # Get input file path
    checkboxX=ScriptUtil.findWidgetByName(widget, "Check Box X Stored")
    checkboxY=ScriptUtil.findWidgetByName(widget, "Check Box Y Stored")
    checkboxDiffX=ScriptUtil.findWidgetByName(widget, "Check Box X Difference")
    checkboxDiffY=ScriptUtil.findWidgetByName(widget, "Check Box Y Difference")

    file_path = PVUtil.getString(ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "file_path")))
    if (file_path == ""):
        ScriptUtil.showMessageDialog(widget,
        "Specify input file path.")
        return False
    
    
    acquiredate=ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget,"AcquiredDate"))
    #root_widget = ScriptUtil.findWidgetByName(widget,"AcquiredDate").root
    # Write selected file to widget
    file_path_pv = ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget,"file_path"))
    file_path_pv.setValue(file_path)
    pvs = None
    # Read file contents and try to deserialize them
    try:
        percorso_assoluto = os.path.abspath(file_path)
        logger.info("opening " +percorso_assoluto )
        with open(percorso_assoluto, 'r') as file:
            data = file.read()

        #data = FileUtil.readTextFile(file_path, widget)
            #logger.info("Data " + data)
        
            deserializer = Deserializer(data)
            pvs = deserializer.deserialize()
    except :
        ScriptUtil.showErrorDialog(widget, "Could not load PV values from file:\n" + percorso_assoluto + "\n\nMake sure you are trying to load the correct file: ")
        return False

    #prompt = ScriptUtil.showConfirmationDialog(widget,"Load trajectory from file?\n" + percorso_assoluto)
    #if (prompt != True):
    #    return False
   

    # Traces that will contain values loaded from file start at index 2
    i_trace = 2
    graph =  ScriptUtil.findWidgetByName(widget, "aggregator_graph_2")
    

    
    
    #pvs = deserializer.deserialize()
    logger.info("deserialized: "+str(pvs))
    timestring=""
    for pv in pvs:
        logger.info("pv '"+pv['name'] + "' ts:"+pv['ts'] + " len:"+str(len(pv['data'])))
        timestring=pv['ts']
        if pv['name'].endswith("y"):
            loc_pv_y = PVUtil.createPV("loc://stored_y<VDoubleArray>", 1)
            #loc_pv_y= ScriptUtil.getPVByName(graph,"loc://stored_y")
            if loc_pv_y:
                loc_pv_y.write(pv['data'])
        if pv['name'].endswith("x"):
            loc_pv_y=  PVUtil.createPV("loc://stored_x<VDoubleArray>", 1)
            if loc_pv_y:
                loc_pv_y.write(pv['data'])

       

    
    #trace_visibility.setValue(1)
    acquiredate.setValue("Last Saved Data:"+ timestring)
    #root_widget.update()
    ScriptUtil.showMessageDialog(widget, "Trajectory successfully loaded from file:\n" + percorso_assoluto)
    checkboxX.setPropertyValue("enabled",True)
    checkboxY.setPropertyValue("enabled",True)
    checkboxDiffX.setPropertyValue("enabled",True)
    checkboxDiffY.setPropertyValue("enabled",True)
    return True


main()
