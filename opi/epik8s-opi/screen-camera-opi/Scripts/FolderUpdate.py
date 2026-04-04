from java.util import Date
from java.text import SimpleDateFormat
#from java.lang import Thread
from org.csstudio.display.builder.runtime.script import PVUtil
from org.csstudio.display.builder.runtime.script import ScriptUtil
import os

logger = ScriptUtil.getLogger()

# Get current date
date = Date()

# Format date string as YYYY_MM_DD
FolderName = SimpleDateFormat("yyyy_MM_dd")
date_string = FolderName.format(date)
SubFolderName = SimpleDateFormat("HH'h'_mm'm'_ss's'")
time_string = SubFolderName.format(date)

update_dir = PVUtil.getDouble(pvs[1])

if update_dir==1:
    mycam = widget.getEffectiveMacros().getValue("CAM")
    fname="/nfs/data/"+date_string+"/"+mycam+"/"+time_string
    pvs[0].write(fname);
    logger.info("Generated folder name: " + fname);
    #Thread.sleep(500)  # argument is in milliseconds
    #at the end put back to 0
    pvs[1].write(0);
else:
	pass
