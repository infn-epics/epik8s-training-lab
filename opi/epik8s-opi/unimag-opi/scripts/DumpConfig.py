from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from confutil import csv_to_list
from org.csstudio.display.builder.model import WidgetFactory
import os

# logger = ScriptUtil.getLogger()
device_prefix = widget.getEffectiveMacros().getValue("P")

# logger.info("device " +device_prefix )
if not device_prefix:
    device_prefix = "NOPREFIX"

# Replace pvs[0] with ScriptUtil.getPrimaryPV
primary_pv = ScriptUtil.getPrimaryPV(widget)
if primary_pv is None:
    raise ValueError("Primary PV is not defined.")

name = PVUtil.getString(primary_pv)

print("Loading: " + name + " from " + str(primary_pv))

embedded_width = 570
embedded_height = 35
offy = 40
if name:
    print("selected path:" + name)
    data_dict = {}
    cnt = 0
    display_model = widget.getDisplayModel()

    conffile = widget.getEffectiveMacros().getValue("CONFFILE")
    display_path = os.path.dirname(display_model.getUserData(display_model.USER_DATA_INPUT_FILE))

    confpath = display_path + "/" + conffile

    if not os.path.exists(confpath):
        ScriptUtil.showMessageDialog(widget, "Cannot find file \"" + confpath + "\" please set CONFFILE macro to a correct file")

    # Parse conf file

    fcsvn= name + ".sar.csv"
    fcsvn_value_name= name + ".value.csv"

    print("Generating:" + fcsvn)

    # Open a file for writing
    fcsv = open(fcsvn, 'w')
    fcsvn_value = open(fcsvn_value_name, 'w')

    fcsv.write("PV,READBACK,READ_ONLY\n")
    fcsvn_value.write("Name,Prefix,Current,State\n")
    
    devinfo = csv_to_list(confpath)

    with open(name, 'r') as file:
        # Loop over the 16 PVs and write their values to the file
        if name.endswith(".dat"):
            # Assume it's an old data format
            for line in file:
                parts = line.split()
                # Ensure there are exactly 4 parts for each line
                if len(parts) == 4:
                    identifier = parts[0]
                    value = float(parts[1])
                    pol = parts[2]
                    status = int(parts[3])  # Convert to int for count
                    data_dict[identifier] = {
                        'value': value,
                        'pol': pol,
                        'status': status
                    }
                    print("parsed : " + identifier + "=" + str(data_dict[identifier]))
                    loc_current = None
                    loc_state = None
                    prefix = device_prefix
                    found = False
                    for d in devinfo:
                        if d['Name'] == identifier:
                            if 'Prefix' in d:
                                prefix = d['Prefix']
                            found = True
                            pv_prefix = prefix + ":" + identifier

                    if not found:
                        print("%% not found: " + identifier + " in " + conffile)
                        continue
                    
                    fcsv.write(pv_prefix + ":current," + pv_prefix + ":current_rb,0\n")
                    fcsv.write(pv_prefix + ":state," + pv_prefix + ":state_rb,0\n")
                    try:
                        remote_current = PVUtil.createPV(pv_prefix + ":current_rb", 100)
                        remote_state = PVUtil.createPV(pv_prefix + ":state_rb", 100)
                        fcsvn_value.write(identifier + "," + prefix + "," + str(remote_current.read().getValue()) + "," + str(remote_state.read().getValue()) + "\n")
                    except (Exception, lang.Exception) as e:
                        print("## Error Reading " + pv_prefix + " " + str(e))
                        ScriptUtil.showMessageDialog(widget, "## Error reading " + pv_prefix + " " + str(e))
                        


                        
                        
    fcsv.close()
    fcsvn_value.close()
    ScriptUtil.showMessageDialog(widget, "Generated \"" + fcsvn + "\" SAR file & dumped values to \"" + fcsvn_value_name + "\"")
