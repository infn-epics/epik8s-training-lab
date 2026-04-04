from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
from java.lang import Thread
import os

logger = ScriptUtil.getLogger()
folder_path = PVUtil.getString(pvs[0])

make_dir = PVUtil.getDouble(pvs[1])
if make_dir==1: 
	# Create the folder (including parent folders if they don't exist)
    os.makedirs(folder_path,True)
    logger.info("Created folder: " + folder_path)
    Thread.sleep(1000)
    pvs[2].write(folder_path)
    # Write back original (after small delay if necessary)
    #pvs[2].write(folder_path)
    #at the end put back to 0
    pvs[1].write(0);
else:
	pass
