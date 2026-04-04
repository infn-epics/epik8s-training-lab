from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
#from org.epics.pvmanager import PVManager
#from org.epics.pvmanager.data import VTypeHelper
#from org.csstudio.simplepv import PVFactory
import epik8sutil

logger = ScriptUtil.getLogger()
# device_list = epik8sutil.conf_to_dev(widget)

err_val = []
def getZoneIndexes(zoneName):
    return zone.get(zoneName,err_val)

def main():
    xy_plot_widget = ScriptUtil.findWidgetByName(widget, 'aggregator_graph_2')
    macro_value = xy_plot_widget.getEffectiveMacros().getValue("P")

    # Controlla se la macro è stata definita
    if macro_value is None:
        raise Exception("La macro 'P' non è definita")
   
       
    pv_y_name = macro_value+":y"
    coord_pv = macro_value+":coord"
    pv_x_name = macro_value+":x"
    
    pv_x_stored_name = "loc://stored_x"
    pv_y_stored_name = "loc://stored_y"
    pv_x_avg_name = macro_value+":x_avg"
    pv_y_avg_name = macro_value+":y_avg"
    pv_x_std_name = macro_value+":x_std"
    pv_y_std_name = macro_value+":y_std"
    
    coord_pv_y=PVUtil.createPV(coord_pv,1000)
    coord_values=PVUtil.getDoubleArray(coord_pv_y)

    pv_y=PVUtil.createPV(pv_y_name,1000)
    current_value_y = PVUtil.getDoubleArray(pv_y)

    pv_x=PVUtil.createPV(pv_x_name,1000)
    current_value_x = PVUtil.getDoubleArray(pv_x)

    pv_x_stored=PVUtil.createPV(pv_x_stored_name,1000)
    pv_y_stored=PVUtil.createPV(pv_y_stored_name,1000)
    try:
        #if (True):
        pv_x_avg=PVUtil.createPV(pv_x_avg_name,1000)
        pv_x_std=PVUtil.createPV(pv_x_std_name,1000)
        pv_y_std=PVUtil.createPV(pv_y_std_name,1000)
        pv_y_avg=PVUtil.createPV(pv_y_avg_name,1000)
    except Exception as e:
        logger.info("EXCEPTION create: "+ str(e))
        #else:
        pv_x_avg=pv_y_avg=pv_x_std=pv_y_std=None
        
    avg_value_x=None
    avg_value_y=None

    
    std_value_x=None
    std_value_y=None
    avg_available=False

    stored_value_x=None
    stored_value_y=None
    have_stored=False
    try:
            avg_value_x=PVUtil.getDoubleArray(pv_x_avg)
            avg_value_y=PVUtil.getDoubleArray(pv_y_avg)
            std_value_x=PVUtil.getDoubleArray(pv_x_std)
            std_value_y=PVUtil.getDoubleArray(pv_y_std)
            avg_available=True
            stored_value_x=PVUtil.getDoubleArray(pv_x_stored)
            stored_value_y=PVUtil.getDoubleArray(pv_y_stored)
            have_stored=True
            #logger.info("stored x len="+str(len(stored_value_x)))
            if (len(stored_value_x) == 1) or (len(stored_value_y)==1):
                have_stored=False
                #logger.info("set have_stored to "+str(have_stored))
            #logger.info("stored y="+str(stored_value_y))
            if (len(avg_value_x) == 1) or (len(avg_value_y)==1):
                avg_available=False
                #logger.info("set avg_available to "+str(avg_available))

    except Exception as ex:
        logger.info("EXCEPTION: read: " +str(ex))
        have_stored=False
        avg_available=False
        pass

  
    
    #logger.info("Il valore corrente della PV di "+str(len(current_value_x))+" elementi e' "+str(current_value_x))
    selectedAreaName = PVUtil.getString(ScriptUtil.getPrimaryPV(ScriptUtil.findWidgetByName(widget, "Combo Box")))
    # index=getZoneIndexes(selectedAreaName)
        #logger.info("Gli indici da prendere per la zona "+selectedAreaName+" sono "+str(index))
    pv_output_val_y=current_value_y
        #logger.info("Gli indici da prendere per la zona "+selectedAreaName+" sono "+str(index)+"producendo un output "+str(pv_output_val_y))
    pv_output_val_x=current_value_x
    if (have_stored== True):
        pv_output_stored_x=stored_value_x
        pv_output_stored_y=stored_value_y
        #logger.info("pv_out_stored_x= "+ str(pv_output_stored_x))
        pass
    if (avg_available == True):
        pv_output_avg_x=avg_value_x
        pv_output_avg_y=avg_value_y
        pv_output_std_x=std_value_x
        pv_output_std_y=std_value_y

    # Crea la PV per la scrittura (usando 1 per scrittura)
    pv_write = PVUtil.createPV("loc://yVisual<VDoubleArray>", 1)
    pv_write.write(pv_output_val_y)
    pv_write = PVUtil.createPV("loc://xVisual<VDoubleArray>", 1)
    pv_write.write(pv_output_val_x)
    if (have_stored):
        
        pv_write = PVUtil.createPV("loc://xVisualStored<VDoubleArray>", 1)
        pv_write.write(pv_output_stored_x)
        pv_write = PVUtil.createPV("loc://yVisualStored<VDoubleArray>", 1)
        pv_write.write(pv_output_stored_y)
        pass
    if (avg_available):
        pv_write = PVUtil.createPV("loc://xVisualAvg<VDoubleArray>", 1)
        pv_write.write(pv_output_avg_x)
        pv_write = PVUtil.createPV("loc://yVisualAvg<VDoubleArray>", 1)
        pv_write.write(pv_output_avg_y)

        pv_write = PVUtil.createPV("loc://xVisualStd<VDoubleArray>", 1)
        pv_write.write(pv_output_std_x)
        pv_write = PVUtil.createPV("loc://yVisualStd<VDoubleArray>", 1)
        pv_write.write(pv_output_std_y)

   


main()