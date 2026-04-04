from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
import epik8sutil
from org.phoebus.pv import PVPool
#pvs = ScriptUtil.getPVs(widget)
selection=PVUtil.getLong(pvs[0])

cnt=0
if selection:
    print "**** Selecting all "+str(len(pvs))
else:
    print "**** DEselecting all "+str(len(pvs))
pvs[1].write(0)
devarray = epik8sutil.conf_to_dev(widget)
pvrl=PVPool.getPVReferences()
names=[]
for i in range(len(devarray)):
    n=devarray[i]['P']+":"+devarray[i]['R']
    names.append(n)
for pvr in pvrl:
    entry=pvr.getEntry()
    name=entry.getName()
    if name.startswith("loc://selection:"):
        entry.write(0)
        if selection:
            for sel in names:
                if sel in name:
                    entry.write(1)
                    print "* selecting "+sel
                    cnt+=1
       
pvs[1].write(cnt)
