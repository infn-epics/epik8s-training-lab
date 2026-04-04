from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
from java.lang import Thread

logger = ScriptUtil.getLogger()
mydev = widget.getEffectiveMacros().getValue("DEVICE")
mycam = widget.getEffectiveMacros().getValue("CAM")
prefx=mydev+':'+mycam+":TIFF1:"
start_save = PVUtil.getDouble(pvs[0])

if start_save==1: 
    #start acquire
    pv00=PVUtil.createPV(mydev+':'+mycam+":Acquire",100)
    pv00.setValue(1)
    pv0=PVUtil.createPV(prefx+"FileName",100)
    pv0.setValue("img")
    pv1=PVUtil.createPV(prefx+"FileNumber",100)
    pv1.setValue(0)
    pv2=PVUtil.createPV(prefx+"AutoIncrement",100)
    pv2.setValue(1)
    pv3=PVUtil.createPV(prefx+"FileTemplate",100)
    pv3.setValue("%s%s%3.3d.tiff")
    pv4=PVUtil.createPV(prefx+"FileWriteMode",100)
    pv4.setValue("Capture")
    pv5=PVUtil.createPV(prefx+"AutoSave",100)
    pv5.setValue(0)
    pv6=PVUtil.createPV(prefx+"Capture",100)
    pv7=PVUtil.createPV(prefx+"Capture_RBV",100)
    pv8=PVUtil.createPV(prefx+"NumCapture_RBV",100)
    pv9=PVUtil.createPV(prefx+"NumCaptured_RBV",100)
    pv10=PVUtil.createPV(prefx+"WriteFile",100)
    nimg=PVUtil.getInt(pv8);
    max_attempts=20*nimg
    Thread.sleep(500)
    pv6.setValue(1)

    attempts=0
    while attempts<max_attempts:
        pv_value=PVUtil.getInt(pv9)
        #print(pv_value)
        if pv_value == nimg:
            print("While loop break condition reached")
            Thread.sleep(500)
            pv10.setValue(1)
            print("Images saved!")
            break
        else:
            pass;
        
        attempts += 1
        Thread.sleep(100)  # argument is in milliseconds
    else:
        print("Device not ready after all the attempts")
        pv6.setValue(0) #stop Capture

    #at the end put back to 0
    pvs[0].write(0);
else:
	pass
