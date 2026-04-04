from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from confutil import csv_to_list
from org.csstudio.display.builder.model import WidgetFactory
from org.phoebus.pv import PVPool

import os
savedirw =ScriptUtil.findWidgetByName(widget,"DirSave")
filenw=ScriptUtil.findWidgetByName(widget,"FileSave")
savedir = PVUtil.getString(ScriptUtil.getPrimaryPV(savedirw))
filedir = PVUtil.getString(ScriptUtil.getPrimaryPV(filenw))

filename = savedir+"/"+filedir
ffile=open(filename,"w")
ffile.write("Name,Prefix,Current,State\n")

lpvs=PVPool.getPVReferences()
cnt=0
for pvr in lpvs:
    remote=pvr.getEntry()
    name=remote.getName()

    if name.startswith("loc://selection:"):
        if remote.read().getValue()==1:
            pv_prefix=name.replace("loc://selection:","")
            ## Name is the last part of rname till the first :
            
            prefix,identifier=pv_prefix.rsplit(":",1)
            try:
                remote_current = PVUtil.createPV(pv_prefix + ":current_rb", 100)
                remote_state = PVUtil.createPV(pv_prefix + ":state_rb", 100)
                ffile.write(identifier + "," + prefix + "," + str(remote_current.read().getValue()) + "," + str(remote_state.read().getValue()) + "\n")
            except (Exception, lang.Exception) as e:
                print("## Error Reading " + pv_prefix + " " + str(e))
                ScriptUtil.showMessageDialog(widget, "## Error reading " + pv_prefix + " " + str(e))
ffile.close()
ScriptUtil.showMessageDialog(widget, "Saved as "+filename)

