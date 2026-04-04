from org.csstudio.opibuilder.scriptUtil import PVUtil, FileUtil, ConsoleUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
from org.csstudio.display.builder.runtime.pv import PVFactory

#from java.lang import Exception
from PV2File import Serializer
import os
logger = ScriptUtil.getLogger()
zone_dict = {
    "All": (0.0, 31000.0),
    "LINAC": (600, 9000),
    "LINAC-DOODLEG": (600, 31000),
    "LINAC-UNDULATOR": (600, 17240),
    "DOODLEG": (22000,31000),
    "EXIN": (15000, 21000)
}
err_val = (0.0, 0.0)

def getGraphLimits(zone):
    return zone_dict.get(zone,err_val)

def main():
    
    selectedAreaName = PVUtil.getString(ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "Combo Box")))
    #logger.info(" Chosed area: '" + selectedAreaName+"'")
    
    grafo=ScriptUtil.findWidgetByName(widget, "aggregator_graph")
    grafo.setPropertyValue('x_axis.minimum', getGraphLimits(selectedAreaName)[0])
    grafo.setPropertyValue('x_axis.maximum', getGraphLimits(selectedAreaName)[1])
   


    grafo=ScriptUtil.findWidgetByName(widget, "aggregator_graph_1")
    grafo.setPropertyValue('x_axis.minimum', getGraphLimits(selectedAreaName)[0])
    grafo.setPropertyValue('x_axis.maximum', getGraphLimits(selectedAreaName)[1])
   
    return True

main()