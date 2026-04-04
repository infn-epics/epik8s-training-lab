from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from org.csstudio.display.builder.model import WidgetFactory
import os
import epik8sutil
from javax.swing import JOptionPane
from java.awt.datatransfer import StringSelection
from java.awt import Toolkit

epik8sutil.dump_selected_tofile(widget)
# clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
# clipboard.setContents(StringSelection(listpv), None)

# # Show dialog with title and copiable content
# JOptionPane.showMessageDialog(None, listpv, "PV List copied to clipboard", JOptionPane.INFORMATION_MESSAGE)