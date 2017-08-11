# -*- coding: utf-8 -*- 
import csv
import datetime
from SiteCell import *
from Train import *

CellNumPerMinute = 8

TrainList = []
f = open('timetable(interval5).csv', 'rU')

reader = csv.reader(f)
for i,row in enumerate(reader):
	TrainList.append(Train(i,[]))
	for time in row:
		TrainList[i].TimeTable.append(datetime.datetime.strptime(time, '%H:%M:%S'))

	#print TrainList[i].TimeTable
f.close()

#Line state setting
StationNum = 19
interStationMinutes = 3

LineState = []
LineState.append(SiteCell(True,0,0,False))
for i in range(1,StationNum):
	for j in range(0,interStationMinutes*CellNumPerMinute):
		LineState.append(SiteCell(False,0,None,False))
	LineState.append(SiteCell(True,0,i,False))	

#Time Control
current = datetime.datetime(100,1,1,4,50,00)
timePerStep = datetime.timedelta(seconds=60/CellNumPerMinute) 
end = datetime.datetime(100,1,1,5,30,00)

isForward = False
while current <= end:
	for i in range(0,1):
		if TrainList[i].CurrentStop < StationNum: #Halfway
			# arrive
			if TrainList[i].CurrentStop != -1 and current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2-1].time():
				isForward = False
			
			# deperture (updating destination station)
			if TrainList[i].CurrentStop == -1 and current.time() >= TrainList[i].TimeTable[0].time():
			#starting depot to starting station
					TrainList[i].CurrentStopUpdate()
					TrainList[i].CurrentSiteUpdate()
					TrainList[i].ConvertOperationMode()	#F->T
					isForward = True

					LineState[0].existTrain = True			
			elif current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2].time():
				TrainList[i].CurrentStopUpdate()
				isForward = True
		elif TrainList[i].CurrentStop == StationNum: #Terminal station
			if current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2].time():
				TrainList[i].CurrentStopUpdateToDepot()
	  			TrainList[i].ConvertOperationMode() #T->F
				isForward = False
				
		if TrainList[i].InOperation and isForward:
			LineState[TrainList[i].CurrentSite].existTrain = False
			TrainList[i].CurrentSiteUpdate()
			LineState[TrainList[i].CurrentSite].existTrain = True
		
		print current.time(),TrainList[i].TrainNum,TrainList[i].CurrentStop,TrainList[i].CurrentSite,isForward
		
	current += timePerStep
	
"""
for i in range(0,len(LineState)):
	print i,LineState[i].existTrain,LineState[i].isStation
"""

