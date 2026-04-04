from org.csstudio.opibuilder.scriptUtil import PVUtil, FileUtil, DataUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
import os
from java.lang import Exception

from PV2File import Deserializer
logger = ScriptUtil.getLogger()

def main():
    # Get input file path
    file_path = PVUtil.getString(ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "file_path")))
    if (file_path == ""):
        ScriptUtil.showMessageDialog(widget,
        "Specify input file path.")
        return False
    
    # Get Trace Visibility PV. We'll set this to '1' after 
    # successfully loading values from file.
    trace_visibility = ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget,"VisualizeStored"))
    acquiredate=ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget,"AcquiredDate"))
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
            logger.info("Data " + data)
        
            deserializer = Deserializer(data)
            pvs = deserializer.deserialize()
    except :
        ScriptUtil.showErrorDialog(widget, "Could not load PV values from file:\n" + percorso_assoluto + "\n\nMake sure you are trying to load the correct file: ")
        return False

    prompt = ScriptUtil.showConfirmationDialog(widget,"Load trajectory from file?\n" + percorso_assoluto)
    if (prompt != True):
        return False
   

    # Traces that will contain values loaded from file start at index 2
    i_trace = 2
    graph =  ScriptUtil.findWidgetByName(widget, "aggregator_graph")
    graph1 =  ScriptUtil.findWidgetByName(widget, "aggregator_graph_1")

    
    
    pvs = deserializer.deserialize()
    logger.info("deserialized: "+str(pvs))
    timestring=""
    for pv in pvs:
        logger.info("pv '"+pv['name'] + "' ts:"+pv['ts'] + " len:"+str(len(pv['data'])))
        timestring=pv['ts']
        loc_pv= ScriptUtil.getPVByName(graph,"loc://"+pv['name'])
        if loc_pv:
            loc_pv.setValue(pv['data'])

        loc1_pv= ScriptUtil.getPVByName(graph1,"loc://"+pv['name'])
        if loc1_pv:
            loc1_pv.setValue(pv['data'])

    
    trace_visibility.setValue(1)
    acquiredate.setValue("Acquired on:"+ timestring)
    return True


main()
