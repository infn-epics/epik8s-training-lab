from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from confutil import csv_to_list
from org.csstudio.display.builder.model import WidgetFactory
import os
def createInstance(x, y,macros):
    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget()
    embedded.setPropertyValue("name", "item-"+str(y/embedded_height))

    embedded.setPropertyValue("x", x)
    embedded.setPropertyValue("y", y)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in macros.items():
            embedded.getPropertyValue("macros").add(macro, value)

    embedded.setPropertyValue("file", "MagnetChannelSet.bob")
    return embedded

# logger = ScriptUtil.getLogger()
device_prefix = widget.getEffectiveMacros().getValue("P")

# logger.info("device " +device_prefix )
if not device_prefix:
    device_prefix="NOPREFIX"
    
name = PVUtil.getString(pvs[0])

# pv = ScriptUtil.getPrimaryPV(filename)
# name = PVUtil.getString(pv)
print "Loading: "+name
#dataset =  ScriptUtil.findWidgetByName(widget, "DataSet")
#loadset = ScriptUtil.findWidgetByName(widget, "LoadSetting")
#loadset.setPropertyValue("enabled",False)

wtemplate = ScriptUtil.findWidgetByName(widget, "element_template") ## name of the hidden template

interlinea=5

embedded_width  = wtemplate.getPropertyValue("width")
embedded_height = wtemplate.getPropertyValue("height") +interlinea
offy=0
cnt=0

if name:
    if name.endswith(".csv"):
        ## new syntax Name, Prefix, Current, State
        devinfo = csv_to_list(name)
        for d in devinfo:
            x=0
            y= offy+ cnt * (embedded_height)
            
            prefix=d['Prefix']
            identifier=d['Name']
            m={'R': identifier,'P': prefix}
            print("ELE "+str(d))
            instance = createInstance(x, y, m)
            widget.runtimeChildren().addChild(instance)
            loc_current = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":current",10)
            loc_state = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":state",10)
            loc_current_ok = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":current:ok",10)
            loc_state_ok = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":state:ok",10)
            loc_current.write(d['Current'])
            loc_state.write(d['State'])
            loc_current_ok.write(1)
            loc_state_ok.write(1)

            # if d['State']=="ON":
            #     loc_state.write(1)
            # else:
            #     loc_state.write(2)

            cnt=cnt+1
        
    else:
        #os.makedirs(os.path.dirname(name), exist_ok=True)
        print "selected path:"+name + " embedded_width:"+str(embedded_width) + " embedded_height:"+str(embedded_height)
        data_dict = {}
        # dataset.setPropertyValue("name", os.path.basename(name))
        # Open the file for writing
        display_model = widget.getDisplayModel()

        conffile = widget.getEffectiveMacros().getValue("CONFFILE")
        display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))

        confpath = display_path + "/" + conffile

        if not os.path.exists(confpath):
            ScriptUtil.showMessageDialog(widget, "Cannot find file \"" + confpath + "\" please set CONFFILE macro to a correct file")

    # Parse conf file
        print("LOADING:" + confpath)

        devinfo = csv_to_list(confpath)
        with open(name, 'r') as file:
            # Loop over the 16 PVs and write their values to the file
            if name.endswith(".dat"):
                ## assume its a old data format
                for line in file:
                    parts = line.split()  
                    # Ensure there are exactly 4 parts for each line
                    if len(parts) == 4:
                        identifier = parts[0]
                        value = float(parts[1])     
                        pol = parts[2]
                        status = int(parts[3])        # Convert to int for count
                        data_dict[identifier] = {
                            'value': value,
                            'pol': pol,
                            'status': status
                        }
                        print "parsed : "+identifier+"="+ str(data_dict[identifier] )
                        loc_current= None
                        loc_state= None
                        prefix=device_prefix
                        found=False
                        for d in devinfo:
                            if d['Name'] == identifier:
                                if 'Prefix' in d:
                                    prefix = d['Prefix']
                                found=True
                                loc_current = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":current",10)
                                loc_state = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":state",10)
                                loc_current_ok = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":current:ok",10)
                                loc_state_ok = PVUtil.createPV("loc://apply:unimag:"+prefix+":"+identifier+":state:ok",10)
                                loc_current_ok.write(1)
                                loc_state_ok.write(1)
                        if not found:
                            print "%% not found: "+identifier + " in "+conffile
                            continue
                        #pvn="loc://apply:"+device_prefix+":"+identifier
                        #loc_pv = PVUtil.createPV(pvn+":current",1)
                        # value = PVUtil.getString(pv)
                        # value = PVUtil.getString(pv)
                        
                        
                        x=0
                        y= offy+ cnt * embedded_height 
                        m={'R': identifier,'P': prefix}
                        cnt=cnt+1
                        instance = createInstance(x, y, m)
                        widget.runtimeChildren().addChild(instance)
                        #loc_current=ScriptUtil.getPVByName(instance,"loc://apply:"+prefix+":"+identifier+":current")
                        #loc_state=ScriptUtil.getPVByName(instance,"loc://apply:"+prefix+":"+identifier+":state")

                        if pol=="+":
                            pol=1
                            loc_current.write(abs(value))

                        elif pol=="-":
                            pol=-1
                            loc_current.write(-abs(value))

                        elif pol=="*":
                            pol=0
                        else:
                            pol=3
                        
                        if pol==0:
                            loc_current.write(0)
                            loc_state.write("STANDBY") ## standby
                        else:
                            loc_state.write("ON") ## on
                        #dataset.setPropertyValue("height", y+5)
    
