from org.csstudio.opibuilder.scriptUtil import PVUtil,ScriptUtil

graph = ScriptUtil.findWidgetByName(widget,"Oscilloscope Display").setPropertyValue
#graph = display.getWidget("Oscilloscope Display").setPropertyValue

P = widget.getEffectiveMacros().getValue("P")

pvChosen=PVUtil.createPV("loc://"+P+":CH1_VISIBLE",1000)
check1 =PVUtil.getInt(pvChosen)
pvChosen=PVUtil.createPV("loc://"+P+":CH2_VISIBLE",1000)
check2 =PVUtil.getInt(pvChosen)
pvChosen=PVUtil.createPV("loc://"+P+":CH3_VISIBLE",1000)
check3 =PVUtil.getInt(pvChosen)
pvChosen=PVUtil.createPV("loc://"+P+":CH4_VISIBLE",1000)
check4 =PVUtil.getInt(pvChosen)

pvChosen=PVUtil.createPV("loc://"+P+":CH5_VISIBLE",1000)
check5 =PVUtil.getInt(pvChosen)
pvChosen=PVUtil.createPV("loc://"+P+":CH6_VISIBLE",1000)
check6 =PVUtil.getInt(pvChosen)
pvChosen=PVUtil.createPV("loc://"+P+":CH7_VISIBLE",1000)
check7 =PVUtil.getInt(pvChosen)
pvChosen=PVUtil.createPV("loc://"+P+":CH8_VISIBLE",1000)
check8 =PVUtil.getInt(pvChosen)
#check1 = display.getWidget("Check_Box_CH1").getValue()
#check2 = display.getWidget("Check_Box_CH2").getValue()
#check3 = display.getWidget("Check_Box_CH3").getValue()
#check4 = display.getWidget("Check_Box_CH4").getValue()

if (check1 == 0):
	graph("traces[0].visible", "false")
else:
	graph("traces[0].visible", "true")
	
if (check2 == 0):
	graph("traces[1].visible", "false")
else:
	graph("traces[1].visible", "true")

if (check3 == 0):
	graph("traces[2].visible", "false")
else:
	graph("traces[2].visible", "true")

if (check4 == 0):
	graph("traces[3].visible", "false")
else:
	graph("traces[3].visible", "true")


if (check5 == 0):
	graph("traces[4].visible", "false")
else:
	graph("traces[4].visible", "true")
	
if (check6 == 0):
	graph("traces[5].visible", "false")
else:
	graph("traces[5].visible", "true")

if (check7 == 0):
	graph("traces[6].visible", "false")
else:
	graph("traces[6].visible", "true")

if (check8 == 0):
	graph("traces[7].visible", "false")
else:
	graph("traces[7].visible", "true")