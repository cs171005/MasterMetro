# -*- coding: utf-8 -*- 
import csv
import datetime
from Train import *
from LineState import *

CellNumPerMinute = 4

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

LineState = LineState()
LineState.append(SiteCell(True,0,0,False))
for i in range(1,StationNum):
	for j in range(0,interStationMinutes*CellNumPerMinute-1):
		LineState.append(SiteCell(False,0,None,False))
	LineState.append(SiteCell(True,0,i,False))	

#Time Control
current = datetime.datetime(100,1,1,4,55,00)
timePerStep = datetime.timedelta(seconds=60/CellNumPerMinute) 
end = datetime.datetime(100,1,1,8,30,00)

firstTrainNum = 0
for i in range(0,len(TrainList)):
	if (TrainList[i].TimeTable[0] - datetime.timedelta(seconds=30)).time() < current.time():
		firstTrainNum += 1

trouble = True
troubleStart = datetime.datetime(100,1,1,7,30,00)
troubleEnd = datetime.datetime(100,1,1,7,45,00)
arrive = datetime.datetime(100,1,1,7,30,00) #dummy init
while current <= end:
	for i in range(firstTrainNum,len(TrainList)):
		#Incident 
		if trouble:
			if troubleStart <= current <= troubleEnd:
				break
			
		if TrainList[i].CurrentStop < StationNum-1: #Starting and Halfway statitons
			# ARRIVE
			if TrainList[i].CurrentStop != -1 and current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2-1].time() and TrainList[i].CurrentSite == CellNumPerMinute*interStationMinutes*TrainList[i].CurrentStop:
				TrainList[i].isForward = False
				arrive = current
			elif TrainList[i].CurrentStop == -1 and current.time() >= (TrainList[i].TimeTable[0] - datetime.timedelta(seconds=30)).time():
			#starting depot to starting station
					TrainList[i].CurrentStopUpdate()
					TrainList[i].CurrentSiteUpdate()
					TrainList[i].ConvertOperationMode()	#F->T
					TrainList[i].isForward = False
					LineState.state[TrainList[i].CurrentSite].existTrain = True
					arrive = current
			# DEPERTURE (updating destination station)
			if TrainList[i].CurrentStop == -1 and current.time() >= TrainList[i].TimeTable[0].time():
			#starting depot to starting station
					TrainList[i].CurrentStopUpdate()
					TrainList[i].CurrentSiteUpdate()
					TrainList[i].ConvertOperationMode()	#F->T
					TrainList[i].isForward = True

					LineState.state[0].existTrain = True			
			elif current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2].time():
			#deperture from stations in halfway.
				if LineState.state[TrainList[i].CurrentSite+1].existTrain == False: #Collision prevention
					TrainList[i].CurrentStopUpdate()
					TrainList[i].isForward = True
		
		elif TrainList[i].CurrentStop == StationNum-1: #terminal station
		# ARRIVE
			if TrainList[i].CurrentStop != -1 and current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2-1].time():
				TrainList[i].isForward = False
		# DEPERTURE
		#terminal station to end-side depot
			if current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2].time():
				LineState.state[TrainList[i].CurrentSite].existTrain = False
				TrainList[i].CurrentStopUpdateToDepot()
				TrainList[i].CurrentSiteUpdateToDepot()				
	  			TrainList[i].ConvertOperationMode() #T->F
				TrainList[i].isForward = False
			
		#move to the next site cell (represents an inter-section)
		if TrainList[i].InOperation and TrainList[i].isForward and TrainList[i].CurrentSite != 999:
			if LineState.state[TrainList[i].CurrentSite+1].existTrain == False: #Collision prevention
				LineState.state[TrainList[i].CurrentSite].existTrain = False
				TrainList[i].CurrentSiteUpdate()
				LineState.state[TrainList[i].CurrentSite].existTrain = True

	print current.time(),TrainList[0].TrainNum,TrainList[0].CurrentStop,TrainList[0].CurrentSite,TrainList[0].isForward,TrainList[0].InOperation
	LineState.OutputState(current)
	current += timePerStep

os.system('open ' + LineState.outputFile)
	

