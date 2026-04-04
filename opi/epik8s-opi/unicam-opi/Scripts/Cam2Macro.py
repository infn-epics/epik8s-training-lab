from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
from org.csstudio.display.builder.model import DisplayModel 
#from org.csstudio.display.builder.model.macros import macros
logger = ScriptUtil.getLogger()


def main():
    wid =ScriptUtil.findWidgetByName(widget,"Combo Box Camera")
    display_model=wid.getDisplayModel()
    selectedCamera = PVUtil.getString(ScriptUtil.getPrimaryPV(wid))
    current_macro = display_model.getEffectiveMacros().getValue("CAM")
    logger.info("Selected canera " + selectedCamera+ " macro before changing "+current_macro)
    if (selectedCamera != current_macro):
            
            display_model.getPropertyValue("macros").add("CAM", selectedCamera)
            current_macro = display_model.getEffectiveMacros().getValue("CAM")
            logger.info("Selected canera " + selectedCamera+ " macro after  changing "+current_macro)
            
            
            for child in display_model.children:
                    try:
                        
                        widget_type = child.getPropertyValue("type") 
                        logger.info(child.name + " of type "+widget_type)
                        if widget_type == "tabs":
                              #tabs = child.getTabs() 
                              logger.info(str(dir(child)))
                              #logger.info(str(child.children.name))
                              for tab in tabs:
                                     logger.info(tab.name)
                                     #fil=tab.children.getPropertyValue("file")
                                     #tab.children.getPropertyValue("macros").add("CAM", selectedCamera)
                                     #tab.children.setPropertyValue("file","")
                                     #tab.children.setPropertyValue("file",fil)
                                    
                        fil=child.getPropertyValue("file")
                        child.getPropertyValue("macros").add("CAM", selectedCamera)
                        child.setPropertyValue("file","")
                        child.setPropertyValue("file",fil)
                        

                    except:
                        #logger.info(str(dir(child)))
                        logger.info("has excepted")
                        continue


        


  
    #print (dir(display_model))
    pass




main()