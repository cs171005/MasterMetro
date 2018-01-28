# -*- coding: utf-8 -*-
import csv
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

from Train import *
from LineState import *

#Line state setting
StationNum = 19
interStationMinutes = 3
CellNumPerMinute = 4

TrainList = []
#Loading timetable from csv file.
f = open('timetable(interval5).csv', 'rU')
reader = csv.reader(f)
for i,row in enumerate(reader):
	TrainList.append(Train(i,[]))
	for time in row:
		TrainList[i].TimeTable.append(datetime.datetime.strptime(time, '%H:%M:%S'))

	#print TrainList[i].TimeTable
f.close()

# random.seed(1)
#Line up SiteCell
LineState = LineState()
LineState.append(SiteCell(True,0,0,False))
for i in range(1,StationNum):
	for j in range(0,interStationMinutes*CellNumPerMinute-1):
		LineState.append(SiteCell(False,i,None,False)) #represents interstation
	LineState.append(SiteCell(True,i,i,False)) #represents stations

# print LineState.hopProb
for site in LineState.state:
	site.siteHopProbUpdate(LineState.hopProb)

# for i,site in enumerate(LineState.state):
# 	print i,site.isStation, site.segmentationNumber, site.hopProb

#Time Control
current = datetime.datetime(100,1,1,4,55,00)
timePerStep = datetime.timedelta(seconds=60/CellNumPerMinute)
end = datetime.datetime(100,1,1,13,10,00)

firstTrainNum = 0 #this number represents the first train number whose behavior is simulated in this simulation.
for i in range(0,len(TrainList)):
	if (TrainList[i].TimeTable[0] - datetime.timedelta(seconds=30)).time() < current.time():
		firstTrainNum += 1

#MAIN BODY
while current <= end:
	LineState.setHopProb(current)
	for i in range(firstTrainNum,len(TrainList)):
		if TrainList[i].CurrentStop < StationNum-1: #ARRIVE and DEPERTURE at Starting and Halfway statitons
			# ARRIVE
			if TrainList[i].CurrentStop != -1 and LineState.state[TrainList[i].CurrentSite].isStation == True:
			#arrive at halfway stations
				if TrainList[i].isForward:
					TrainList[i].arriveUpdate(current)
					TrainList[i].MeasureDelay(current)

				TrainList[i].isForward = False
			elif TrainList[i].CurrentStop == -1 and current.time() >= (TrainList[i].TimeTable[0] - datetime.timedelta(seconds=30)).time():
			#starting depot to starting station
					TrainList[i].CurrentStopUpdate()
					TrainList[i].CurrentSiteUpdate()
					TrainList[i].ConvertOperationMode()	#F->T
					TrainList[i].isForward = False
					LineState.state[TrainList[i].CurrentSite].existTrain = True
					TrainList[i].arriveUpdate(current)
			# DEPERTURE (updating destination station)
			if TrainList[i].CurrentStop == -1 and current.time() >= TrainList[i].TimeTable[0].time():
			#starting depot to starting station
					TrainList[i].CurrentStopUpdate()
					TrainList[i].CurrentSiteUpdate()
					TrainList[i].ConvertOperationMode()	#F->T
					TrainList[i].isForward = True

					LineState.state[0].existTrain = True
			elif LineState.state[TrainList[i].CurrentSite].isStation and current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2].time() and current.time() >= (TrainList[i].arrive + datetime.timedelta(seconds=30)).time():
			#deperture from stations in halfway.
				if LineState.state[TrainList[i].CurrentSite+1].existTrain == False: #Collision prevention
					TrainList[i].CurrentStopUpdate()
					TrainList[i].isForward = True

		elif TrainList[i].CurrentStop == StationNum-1: #ARRIVE and DEPERTURE at terminal station
		# ARRIVE
			if TrainList[i].CurrentStop != -1 and current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2-1].time():
				TrainList[i].isForward = False
				if not TrainList[i].arrivedFinalStop:
					TrainList[i].MeasureDelay(current)
					TrainList[i].arrivedFinalStop = True

		# DEPERTURE
		#terminal station to end-side depot
			if current.time() > TrainList[i].TimeTable[TrainList[i].CurrentStop*2].time():
				LineState.state[TrainList[i].CurrentSite].existTrain = False
				TrainList[i].CurrentStopUpdateToDepot()
				TrainList[i].CurrentSiteUpdateToDepot()
	  			TrainList[i].ConvertOperationMode() #T->F
				TrainList[i].isForward = False

		#move to the next site cell (represents an inter-section)
		#print LineState.state[TrainList[i].CurrentSite].segmentationNumber, LineState.hopProb[LineState.state[TrainList[i].CurrentStop].segmentationNumber]
		if TrainList[i].InOperation and TrainList[i].isForward and TrainList[i].CurrentSite != 999:
			if LineState.state[TrainList[i].CurrentSite+1].existTrain == False: #Collision prevention
				if random.random() <= LineState.state[TrainList[i].CurrentSite].hopProb: #Probably control
					LineState.state[TrainList[i].CurrentSite].existTrain = False
					TrainList[i].CurrentSiteUpdate()
					LineState.state[TrainList[i].CurrentSite].existTrain = True

	# print current.time(),TrainList[26].TrainNum,TrainList[26].CurrentStop,TrainList[26].CurrentSite,TrainList[26].arrive.time(),TrainList[26].isForward,TrainList[26].InOperation
	LineState.OutputState(current)
	current += timePerStep
#MAIN BODY↑↑
os.chdir("/Users/ev30112/Dropbox/programming/MasterMetro/MasterMetroViewer/data")
outputFile = 'delaylog-'+datetime.datetime.now().strftime('%y%m%d-%H%M%S')+'.txt'

if os.path.exists(outputFile):
	f = open(outputFile,'a')
else:
	f = open(outputFile,'w')

for t in TrainList:
	f.write(str(t.delaySecList) + '\n')

f.flush()
f.close()

delayall = []
delaymean = []
for t in TrainList:
	delayall.extend(t.delaySecList)
	delaymean.append(np.mean(t.delaySecList))

delayall.remove(0)
delayall = [item for item in delayall if item is not 0] #remove 0
#print delaymean

os.system('open -a /Applications/TextEdit.app ' + LineState.outputFile)
os.system('open -a /Applications/mi.app ' + outputFile)

plt.hist(delayall,bins=20)
plt.show()

# 箱ひげ図をつくる
'''
fig = plt.figure()
ax = fig.add_subplot(111)
'''
from numpy.random import *

delaymean.remove(0)
delaymean = [item for item in delayall if item is not 0] #remove 0
fig, ax = plt.subplots()
bp = ax.boxplot(delaymean)
plt.title('Box plot')
plt.grid()

plt.xlabel('point')
plt.ylabel('value')
plt.title('Box plot')
plt.show()
