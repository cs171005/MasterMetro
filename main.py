# -*- coding: utf-8 -*- 
import csv
import datetime
from CiteCell import *
from Train import *

CellNumPerMinute = 7

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
LineState.append(CiteCell(True,0,0,False))
for i in range(1,StationNum):
	for j in range(0,interStationMinutes*CellNumPerMinute):
		LineState.append(CiteCell(False,0,None,False))
	LineState.append(CiteCell(True,0,i,False))	

#Time Control
current = datetime.datetime(100,1,1,4,50,00)
timePerStep = datetime.timedelta(seconds=60/CellNumPerMinute) 
end = datetime.datetime(100,1,1,5,30,00)

while current <= end:
	for i in range(0,1):
		if TrainList[i].CurrentStop < StationNum:
			if TrainList[i].CurrentStop == -1 and current.time() >= TrainList[i].TimeTable[0].time():
					TrainList[i].CurrentStopUpdate()				
			elif current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2].time():
				TrainList[i].CurrentStopUpdate()
		elif TrainList[i].CurrentStop == StationNum:
			if current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2].time():
				TrainList[i].CurrentStopUpdateToDeposit()
		print (current.time(),TrainList[i].TrainNum,TrainList[i].CurrentStop)
	current += timePerStep
	


