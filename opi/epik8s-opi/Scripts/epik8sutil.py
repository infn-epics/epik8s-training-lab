from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from java.io import FileReader, BufferedWriter, FileWriter
from org.csstudio.display.builder.model import WidgetFactory

from org.yaml.snakeyaml import Yaml
import os

pvset = {
    'mag': ["STATE_SP","CURRENT_SP"],
    'cool': ["STATE_SP","TEMP_SP"],
    'vac': []
}

pvrb = {
    'mag': ["CURRENT_RB","STATE_RB"],
    'cool': ["TEMP_RB","STATE_RB"],
    'vac': ["PRES_RB"]
}

pvsetrb = {
    'mag': ["STATE","CURRENT"],
    'cool': ["STATE","TEMP"],
}

def _merge_ioc_defaults(ioc_defaults, ioc):
    """Merge iocDefaults template values into an IOC entry. IOC-specific values take precedence."""
    if not ioc_defaults:
        return ioc
    tmpl = ioc.get('template') or ioc.get('devtype') or ''
    if not tmpl:
        return ioc
    tmpl_defaults = ioc_defaults.get(tmpl)
    if tmpl_defaults is None:
        return ioc
    merged = dict(tmpl_defaults)
    merged.update(dict(ioc))
    return merged


def conf_to_iocs(confpath, mywidget):
    """Load the configuration from the YAML file and return the iocs section
    with iocDefaults merged in.
    """
    iocs=[]

    if not os.path.exists(confpath):
        ScriptUtil.showMessageDialog(mywidget, "## Cannot find file \"" + confpath + "\" please set CONFFILE macro to a correct file")
        return iocs
    yaml = Yaml()
    data = yaml.load(FileReader(confpath))
    epics_config = data.get("epicsConfiguration")
    if epics_config is None:
        ScriptUtil.showMessageDialog(mywidget, "Cannot find 'epicsConfiguration' in \"" + confpath + "\"")
        return iocs

    iocs = epics_config.get("iocs")
    if iocs is None:
        ScriptUtil.showMessageDialog(mywidget, "Cannot find iocs section, please provide a valid values.yaml file")
        return iocs

    ioc_defaults = data.get("iocDefaults") or {}
    if ioc_defaults:
        iocs = [_merge_ioc_defaults(ioc_defaults, ioc) for ioc in iocs]

    return iocs


def conf_to_dev(mywidget):
    devarray = []

    pvs = ScriptUtil.getPVs(mywidget)
    zoneSelector = mywidget.getEffectiveMacros().getValue("ZONE")
    typeSelector = mywidget.getEffectiveMacros().getValue("TYPE")
    typeFunc = mywidget.getEffectiveMacros().getValue("FUNC")
    pvzone = None
    pvtype = None
    pvfunc = None
    for pv in pvs:
        if "ZONE" in pv.getName():
            pvzone = pv
        elif "TYPE" in pv.getName():
            pvtype = pv
        elif "FUNC" in pv.getName():
            pvfunc = pv

    if pvzone and zoneSelector == None:
        zoneSelector = PVUtil.getString(pvzone)
    elif zoneSelector is None:
        zoneSelector = "ALL"

    if pvtype and typeSelector == None:
        typeSelector = PVUtil.getString(pvtype)
    elif typeSelector is None:
        typeSelector = "ALL"

    if pvfunc and typeFunc == None:
        typeFunc = PVUtil.getString(pvfunc)
    elif typeFunc is None:
        typeFunc = "ALL"

    forceopi=mywidget.getEffectiveMacros().getValue("OPI")
    
    group=mywidget.getEffectiveMacros().getValue("GROUP")
    conffile = mywidget.getEffectiveMacros().getValue("CONFFILE")
    display_model = mywidget.getDisplayModel()
    display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))

    if conffile is None:
        ScriptUtil.showMessageDialog(mywidget, "## Please set CONFFILE macro to a correct YAML configuration file")
        return devarray
    
    if group == None:
        ScriptUtil.showMessageDialog(mywidget, "## Must Specify group widget (i.e unicool,univac,unimag) (GROUP Macro) \"" + confpath + "\" please set CONFFILE macro to a correct file")
        return devarray
    
    confpath = display_path + "/" + conffile    

    print(mywidget.getName() + "] LOADING \""+group+"\" zoneSelector: \"" + zoneSelector + "\" typeSelector: \"" + str(typeSelector)+"\" typeFunc: \"" + str(typeFunc)+"\" from file \"" + confpath + "\"")

    iocs = conf_to_iocs(confpath,mywidget)
    print(mywidget.getName() + "] Found "+str(len(iocs))+" IOCs in configuration file")

    for ioc in iocs:
        ioc_name = ioc.get("name", "")
        iocprefix = ioc.get("iocprefix", "")
        devtype = ioc.get("devtype", "ALL")
        devgroup = ioc.get("devgroup", "")
        devfunc  = ioc.get("devfun", "")
        opi  = ioc.get("opi", "")
        zones = ioc.get("zones", "ALL")
        iocroot=ioc.get("iocroot", "")

        #print("Checking IOC:", ioc_name, "iocprefix:", iocprefix, "devtype:", devtype)    
        if iocprefix and devgroup == group:
            devices = ioc.get("devices", [])
            # print("Found IOC:", ioc_name, "iocprefix:", iocprefix, "devtype:", devtype, "devices:", len(devices))
            for dev in devices:
                name = dev['name']
                prefix=iocprefix
                devtype=ioc.get("devtype", "ALL")
                iocroot=ioc.get("iocroot", "")
                zones = ioc.get("zones", "ALL")
                pathzone=zones
                
                if 'devfunc' in ioc:
                    devfunc  = ioc.get("devfunc", "")
                else:
                    devfunc = devtype
                    if devgroup == "mag":
                        if ('HCV' in name) or ('HCOR' in name) or ('VCOR' in name) or ('HCR' in name) or ('VCR' in name) or ('CHH' in name) or ('CVV' in name):
                            devfunc="COR"
                        elif ('QUA' in name) or ('QUAD' in name) or ('QSK' in name):
                            devfunc="QUA"
                        elif ('DIP' in name) or ('DPL' in name) or ('DHS' in name) or ('DHR' in name) or ('DHP' in name):
                            devfunc="DIP"
                        elif ('SOL' in name) :
                            devfunc="SOL"
                        elif ('SEX' in name) :
                            devfunc="SEX"
                        elif ('UFS' in name) :
                            devfunc="UFS"
                    if devgroup == "mot":
                        if ('SLT' in name) :
                            devfunc="SLT"
                        elif ('FLG' in name):
                            devfunc="FLG"
                        elif ('MIR' in name) or ('MIR' in iocprefix) :
                            devfunc="MIR"
                        elif ('HMOT' in name) :
                            devfunc="HMOT"
                        elif ('VMOT' in name) :
                            devfunc="VMOT"
                        else:
                            devfunc="MOT"

                        
                    
                    if(devgroup == "vac" and  'SIP' in name):
                        devfunc="ion"
                    

                if 'opi' in dev:
                    opi=dev['opi']
                if 'devtype' in dev:
                    devtype=dev['devtype']
                if 'zones' in dev:
                    zones=dev['zones']
                    if pathzone!="ALL" and isinstance(pathzone, str):
                        zones.append(pathzone)
                if 'name' in dev:
                    if iocroot=="":
                        iocroot=dev['name']
                    else:
                        iocroot=iocroot+":"+dev['name']
                if 'devfun' in dev:
                    devfunc=dev['devfunc']
                if 'alias' in dev:
                    name=dev['alias']
                if 'prefix' in dev:
                    prefix=dev['prefix']
                # print(devgroup_widget+"-"+devtype+" filtering object "+str(dev))

                if zoneSelector and zoneSelector != "ALL" and zoneSelector not in zones:
                    continue
                if typeSelector and typeSelector != "ALL" and typeSelector != devtype:
                    continue
                if typeFunc and typeFunc != "ALL" and typeFunc != devfunc:
                    continue

                if len(zones)==1:
                    zone=zones[0]
                else:
                    zone=str(zones)

                if devfunc == "ion":
                    devfunc = "0"
                elif devfunc == "pig":
                    devfunc = "1"
                elif devfunc == "ccg":
                    devfunc = "2"
                obj={'NAME':name,'R': iocroot, "P": prefix, "FUNC": devfunc,  "TYPE": devtype,"ZONE": zone}
                if forceopi:
                    obj["OPI"] = forceopi
                    print("Forcing OPI \""+forceopi+"\" for device "+name)
                elif opi:
                    obj["OPI"] = opi
                # print("Adding zone:"+str(zones)+"  obj:"+ str(obj))
                devarray.append(obj)
    return devarray

def dump_pv(mywidget,separator="\n"):
    
    """Dump the PVs to a file."""
    devarray = conf_to_dev(mywidget)
    group=mywidget.getEffectiveMacros().getValue("GROUP")

    if not devarray:
        ScriptUtil.showMessageDialog(mywidget, "No devices found for group: " + group)
        return
    pvlist = ""
    for dev in devarray:
        for pv in pvrb.get(group, []):
            pvlist = pvlist + dev['P']+":"+dev['R']+":"+pv+separator
    for dev in devarray:
        for pv in pvset.get(group, []):
            pvlist = pvlist + dev['P']+":"+dev['R']+":"+pv+separator


    return pvlist

def _dump_devices_to_files(mywidget,devarray, group, name):
    """Common function to dump device array to comprehensive files."""
    if not devarray:
        ScriptUtil.showMessageDialog(mywidget, "No devices found for group: " + group)
        return

    sarfile = {}
    sarfiles = ""
    fcsvn_valueset_name = name + ".value_set.csv"
    fcsvn_valuerb_name = name + ".value_rb.csv"
    
    for prop in pvsetrb.get(group, []):
        sarfilen = name + "-" + prop + ".sar.csv"
        sarfiles = sarfiles + sarfilen + "\n"
        sarfile[prop] = open(sarfilen, 'w')
        sarfile[prop].write("PV,READBACK,READ_ONLY\n")

    # Open CSV files for writing
    fcsvn_set = open(fcsvn_valueset_name, 'w')
    fcsvn_rb = open(fcsvn_valuerb_name, 'w')
    fcsvn_set.write("Name,Prefix,PV,Value\n")
    fcsvn_rb.write("Name,Prefix,PV,Value\n")
    
    try:
        for dev in devarray:
            prefix = dev['P'] + ":" + dev['R']
            
            # Process setpoint PVs
            for pv in pvset.get(group, []):
                pvname = prefix + ":" + pv                       
                try:
                    remote_pv = PVUtil.createPV(pvname, 100)
                    val = str(remote_pv.read().getValue())
                    fcsvn_set.write(dev['NAME'] + "," + prefix + "," + pvname + "," + val + "\n")
                except Exception as e:
                    print("Error reading setpoint PV " + pvname + ": " + str(e))
                    fcsvn_set.write(dev['NAME'] + "," + prefix + "," + pvname + ",ERROR\n")
            
            # Process readback PVs  
            for pv in pvrb.get(group, []):
                pvname = prefix + ":" + pv                       
                try:
                    remote_pv = PVUtil.createPV(pvname, 100)
                    val = str(remote_pv.read().getValue())
                    fcsvn_rb.write(dev['NAME'] + "," + prefix + "," + pvname + "," + val + "\n")
                except Exception as e:
                    print("Error reading readback PV " + pvname + ": " + str(e))
                    fcsvn_rb.write(dev['NAME'] + "," + prefix + "," + pvname + ",ERROR\n")
            
            # Process SAR files
            for prop in pvsetrb.get(group, []):
                pv_base = prefix + ":" + prop
                sarfile[prop].write(pv_base + "_SP," + pv_base + "_RB,0\n")

        # Close all files
        for prop in pvsetrb.get(group, []):
            sarfile[prop].close()
        
        fcsvn_set.close()
        fcsvn_rb.close()
        
        ScriptUtil.showMessageDialog(mywidget, "Generated SAR files: " + sarfiles + 
                                   "\nDumped SET values to \"" + fcsvn_valueset_name + 
                                   "\"\nDumped RB values to \"" + fcsvn_valuerb_name + 
                                   "\"\nProcessed " + str(len(devarray)) + " devices")
        
    except Exception as e:
        ScriptUtil.showMessageDialog(mywidget, "Error writing to files: " + str(e))

def dump_selected_tofile(mywidget):
    """Dump the selected PVs to comprehensive files like dump_pv_tofile but using selections."""
    from org.phoebus.pv import PVPool
    
    name=mywidget.getPropertyValue("name")
    group=mywidget.getEffectiveMacros().getValue("GROUP")
    name=ScriptUtil.showSaveAsDialog(mywidget, name)

    if name is None:
        return
    
    print("Dumping selected PVs for group: " + group+ " to file: " + name)
    
    # Get selected devices from PV pool like SetCurrentSelected does
    lpvs = PVPool.getPVReferences()
    selected_devices = []
    
    for pvr in lpvs:
        selection_pv = pvr.getEntry()
        pv_name = selection_pv.getName()
        
        if pv_name.startswith("loc://selection:"):
            if selection_pv.read().getValue() == 1:
                pv_prefix = pv_name.replace("loc://selection:", "")
                prefix, identifier = pv_prefix.rsplit(":", 1)
                
                # Create device entry similar to conf_to_dev format
                dev = {
                    'NAME': identifier,
                    'R': identifier, 
                    'P': prefix,
                    'FUNC': group,  # Use group as function
                    'TYPE': group,  # Use group as type
                    'ZONE': 'SELECTED',
                    'OPI': ''
                }
                selected_devices.append(dev)
    
    if not selected_devices:
        ScriptUtil.showMessageDialog(mywidget, "No devices selected for group: " + group)
        return

    # Use common function to dump files
    _dump_devices_to_files(mywidget, selected_devices, group, name)

def dump_pv_tofile(mywidget):
    """Dump the PVs to a file."""
    name=mywidget.getPropertyValue("name")
    group=mywidget.getEffectiveMacros().getValue("GROUP")
    name=ScriptUtil.showSaveAsDialog(mywidget, name)

    if name is None:
        return

    print("Dumping PVs for group: " + group+ " to file: " + name)
    devarray = conf_to_dev(mywidget)
    
    # Use common function to dump files
    _dump_devices_to_files(mywidget, devarray, group, name)

def load_pv_fromfile(mywidget,name):
    wtemplate = ScriptUtil.findWidgetByName(mywidget, "element_template") ## name of the hidden template
    interlinea=5
    group = mywidget.getEffectiveMacros().getValue("GROUP")
    embedded_width  = wtemplate.getPropertyValue("width")
    embedded_height = wtemplate.getPropertyValue("height") +interlinea
    offy=0
    cnt=0
    bobitem=widget.getEffectiveMacros().getValue("BOBITEM")
    if bobitem is None:
        bobname = "uni"+group+"-opi/"+group + "_channel_load.bob"
    if name.endswith(".csv"):
        # Load the CSV file
        data = csv_to_list(name)
        for row in data:
            pvname = row['PV']
            prefix = row['Prefix']

            value = row['Value']
            local_pv = PVUtil.createPV("loc://apply:"+pvname, 100)
            localok_pv = PVUtil.createPV("loc://apply:"+pvname+":ok", 100)
            local_pv.write(value)
            localok_pv.write(1)
            x=0
            y= offy+ cnt * (embedded_height)
            m={'PVNAME': pvname,"P":prefix,"R":row['Name']}
            instance = createInstance(embedded_width,embedded_height,pvname,bobname,x, y, m)
            mywidget.runtimeChildren().addChild(instance)
            cnt=cnt+1


   
def csv_to_list(csv_file):
    result = []

    with open(csv_file, 'r') as file:
        # Read lines from the file
        lines = file.readlines()
        # Extract the header
        header = [col.strip() for col in lines[0].split(",")]
        # Process each row
        for line in lines[1:]:
            values = [value.strip() for value in line.split(",")]
            row_dict = dict(zip(header, values))
            result.append(row_dict)
    return result


def createInstance(embedded_width,embedded_height,name,bobname,x, y, macros):
    embedded = WidgetFactory.getInstance().getWidgetDescriptor("embedded").createWidget()
    embedded.setPropertyValue("name", "Instance_" + name)

    embedded.setPropertyValue("x", x)
    embedded.setPropertyValue("y", y)
    embedded.setPropertyValue("width", embedded_width)
    embedded.setPropertyValue("height", embedded_height)
    for macro, value in macros.items():
        embedded.getPropertyValue("macros").add(macro, value)

    embedded.setPropertyValue("file", bobname)
    return embedded