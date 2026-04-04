from org.csstudio.opibuilder.scriptUtil import PVUtil, FileUtil, ConsoleUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
from org.csstudio.display.builder.runtime.pv import PVFactory

from java.lang import Exception
from PV2File import Serializer
import os
logger = ScriptUtil.getLogger()


def serializeGraph(fname,graphname,cnt):
   

    # Controlla se la macro è stata definita
    
    graph = ScriptUtil.findWidgetByName(widget, graphname)
    macro_value = graph.getEffectiveMacros().getValue("P")
    if macro_value is None:
        raise Exception("La macro 'P' non è definita")
    for i in ScriptUtil.getPVs(graph):
        #print (str(i))
        if (str(i) == (macro_value+":x")) or (str(i)==(macro_value+":y")): 
            logger.info(fname+" - Serialized '" + str(i)+"'")

            serializer = Serializer(i, str(i))
            data = serializer.serialize()
            FileUtil.writeTextFile(fname, False, widget, data, cnt!=0)
            cnt = cnt+1

def main():
    cnt=0
    #display = widget.getDisplayModel()
    file_path = PVUtil.getString(ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "file_path_save")))
    if not file_path.endswith('/'):
        file_path += '/'
    file_name =PVUtil.getString(ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "Filename Save")))
    logger.info(" - Writing '" + file_path+file_name+"'")
    percorso_assoluto = os.path.abspath(file_path+file_name)
    # Output file path
    #file_path = PVUtil.getString(display.getWidget("file_path").getPV())
    
    # Complain if file path isn't set
    if (percorso_assoluto == ""):
        ScriptUtil.showMessageDialog(widget,
        "Save to file: Output file path must be specified")
        return False
    
    if os.path.isfile(percorso_assoluto):
        prompt = ScriptUtil.showConfirmationDialog(widget,"Overwrite file?\n" + file_path+ file_name)
        if (prompt != True):
            return False
    
    
    # Trace PVs can be retrieved through graph widget and it's traces
    
    serializeGraph(percorso_assoluto,"aggregator_graph_2",0)
    #serializeGraph(percorso_assoluto,"aggregator_graph_1",1)

    #nome= ScriptUtil.getPrimaryPV(graph)
    #logger.info("Name widget " + str(graph))
    #tracey = graph.getPropertyValue("traces[0].y_pv")
    #tracex = graph.getPropertyValue("traces[0].x_pv")


    #pvy = PVFactory.getPV(tracey).read()
    #pvx = PVFactory.getPV(tracex).read()
    #pvx = graph.getPV("X")
    #pvy = graph.getPV("Y")
    #ppy = PVUtil.getDoubleArray(tracey)
    #logger.info("YValues " + str(pvy) + " XValues " + str(pvx)

    # Trace names will be written to file and displayed later when
    # these values are loaded again 
    #pvx_trace_name = graph.getPropertyValue("X")
    #pvy_trace_name = graph.getPropertyValue("Y")
    
    # Overwrite file with first trace PV
    
    # Append second trace PV to file
    #serializer = Serializer(pvy, pvy_trace_name)
    #data = serializer.serialize()
    #FileUtil.writeTextFile(file_path, False, widget, data, True)
    
    # Friendly messagebox to user that values were successfully saved. FileUtil.writeTextFile()
    # should throw an exception if anything goes wrong.
    ScriptUtil.showMessageDialog(widget, "Trajectory successfully saved to file:\n" + percorso_assoluto)
    
    return True


main()
