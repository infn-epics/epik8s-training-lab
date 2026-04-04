from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil
import math;

clight=299792458;
Bang=14*(math.pi)/180; #radians
InputVal=PVUtil.getDouble(pvs[0]);
Bm=1e-4*(55.6+39.5*abs(InputVal)+0.056*InputVal**2-2.78e-4*abs(InputVal)**3);
Lm=0.26748-4.5e-6*abs(InputVal)-5.7e-8*abs(InputVal)**2;
Brad=abs(Lm/Bang);
eGeV=(clight/1e9)*Bm*Brad;
eMeV=eGeV*1000;
mytext="Beam energy: "+str(round(eMeV,1))+" MeV";
widget.setPropertyValue("text", mytext);
