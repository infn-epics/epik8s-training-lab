from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.csstudio.display.builder.model import WidgetFactory
from org.phoebus.pv import PVPool
import os

# logger = ScriptUtil.getLogger()
device_prefix = widget.getEffectiveMacros().getValue("P")

# logger.info("device " +device_prefix )
if not device_prefix:
    device_prefix="NOPREFIX"
    
name = PVUtil.getString(ScriptUtil.getPrimaryPV(widget))
# display=widget.getDisplayModel()
# dataset=display.runtimeChildren().getChildByName("DataSet")
# wgs=display.runtimeChildren().getValue()
# for wg in wgs:
#      print "widget:"+wg.getName()



# pvs= ScriptUtil.getPVs(widget)
# print "Loading PVONES "+ str(r)
pvs=PVPool.getPVReferences()
for pvr in pvs:
    pv=pvr.getEntry()
    name=pv.getName()
    if name.endswith(":ok"):
        continue

    if name.startswith("loc://apply:unimag:") and not name.endswith(":"):
        print ("****** processing "+name)

        local = PVUtil.createPV(name,10)
        localok = PVUtil.createPV(name+":ok",10)
        localok.write(1)

        ## remove the prefix
        rname=name.replace("loc://apply:unimag:","")
        pvread=pv.read().getValue()
        try:
            remote = PVUtil.createPV(rname,100)
            print ("APPLY "+rname+"="+ name+"="+str(pvread))
            #PVUtil.writePV(name+":ok",0,0)
            remote.write(local.read().getValue())
            localok.write(0)
        except:
            print ("## Error APPLING "+rname+"="+ name+"="+str(pvread))

            #PVUtil.writePV(name+":ok",1,0)
            

# pv = ScriptUtil.getPrimaryPV(filename)
# name = PVUtil.getString(pv)
