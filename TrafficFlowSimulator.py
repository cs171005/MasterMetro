# -*- coding: utf-8 -*-
import csv
import datetime
import random
import numpy as np
import pyper

import matplotlib.pyplot as plt

from Train import *
from LineState import *

class TrafficFlowSimulator:
    def __init__(self):
        #Line state setting
        self.StationNum = 19
        self.interStationMinutes = 3
        self.CellNumPerMinute = 4
        self.TrainList = []
        self.LineState = LineState()

        #Loading timetable from csv file.
        f = open('timetable(interval5).csv', 'rU')
        reader = csv.reader(f)
        for i,row in enumerate(reader):
        	self.TrainList.append(Train(i,[]))
        	for time in row:
        		self.TrainList[i].TimeTable.append(datetime.datetime.strptime(time, '%H:%M:%S'))

        self.RecordedTimeTable = [[] for i in range(len(self.TrainList))]
        #print TrainList[i].TimeTable
        f.close()

        # random.seed(1)
        #Line up SiteCell
        self.LineState.append(SiteCell(True,0,0,False))
        for i in range(1,self.StationNum):
        	for j in range(0,self.interStationMinutes*self.CellNumPerMinute-1):
        		self.LineState.append(SiteCell(False,i,None,False)) #represents interstation
        	self.LineState.append(SiteCell(True,i,i,False)) #represents stations
        #LineState.append(SiteCell(False,i,None,False)) #represents interstation

        # print LineState.hopProb
        for site in self.LineState.state:
        	site.siteHopProbUpdate(self.LineState.hopProb)

    def runWithDelayDissatisfactionBool(self, claim_file):
        ttt = self.runWithDelayMatrix()

        bolttt = []
        for row in range(0,len(ttt)):
            blt = []

            for col in range(0,len(ttt[row])):

                if col%2 == 0:
                    #when origin node is the deperture node.
                    station_number = col/2
                    if ttt[row][col] >= claim_file[station_number]["deperture_delay"]:
                        blt.append(True)
                    else:
                        blt.append(False)
                else:
                    #when origin node is the arrive node.
                    station_number = (col+1)/2
                    if ttt[row][col] >= claim_file[station_number]["arrival_delay"]:
                        blt.append(True)
                    else:
                        blt.append(False)
            bolttt.append(blt)
        """
        for row in range(0,len(bolttt)):
            print bolttt[row]
        """
        return bolttt,ttt

    def runWithDelayMatrix(self):
        delayall = []
        delaymean = []
        d_table = []

        self.run()

        for t in self.TrainList:
        	d_row = []
        	# print(str(t.RecordedTime) + '\n')
        	# print len(t.TimeTable[:-1]) == len(t.RecordedTime)
        	for i in range(len(t.RecordedTime)):
        		d = (t.RecordedTime[i] - t.TimeTable[:-1][i]).seconds
        		d_row.append(d)
        		delayall.append(d)
        	d_table.append(d_row)
        """
        for i in range(len(d_table)):
        	print d_table[i]
        """
        return d_table


    def run(self):
        #Time Control
        current = datetime.datetime(100,1,1,4,55,00)
        timePerStep = datetime.timedelta(seconds=60/self.CellNumPerMinute)
        end = datetime.datetime(100,1,1,13,10,00)

        firstTrainNum = 0 #this number represents the first train number whose behavior is simulated in this simulation.
        for i in range(0,len(self.TrainList)):
        	if (self.TrainList[i].TimeTable[0] - datetime.timedelta(seconds=30)).time() < current.time():
        		firstTrainNum += 1

        #MAIN BODY
        while current <= end:
        	self.LineState.setHopProb(current)
        	for i in range(firstTrainNum,len(self.TrainList)): #
        		if self.TrainList[i].CurrentStop < self.StationNum-1: #ARRIVE and DEPERTURE at Starting and Halfway statitons
        			# ARRIVE
        			if self.TrainList[i].CurrentStop != -1 and self.LineState.state[self.TrainList[i].CurrentSite].isStation == True:
        			#arrive at halfway stations
        				if self.TrainList[i].isForward:
        					self.TrainList[i].arriveUpdate(current)
        					self.TrainList[i].MeasureDelay(current)
        					self.RecordedTimeTable[i].append("ARRh:"+str(current - timePerStep))

        				self.TrainList[i].isForward = False
        			elif self.TrainList[i].CurrentStop == -1 and current.time() >= (self.TrainList[i].TimeTable[0] - datetime.timedelta(seconds=30)).time():
        			#starting depot to starting station
        					self.TrainList[i].CurrentStopUpdate()
        					self.TrainList[i].CurrentSiteUpdate()
        					self.TrainList[i].ConvertOperationMode()	#F->T
        					self.TrainList[i].isForward = False
        					self.LineState.state[self.TrainList[i].CurrentSite].existTrain = True
        					self.TrainList[i].arriveUpdate(current)

        					# self.RecordedTimeTable[i].append(""+str(current - timePerStep))
        			# DEPERTURE (updating destination station)
        			if self.TrainList[i].CurrentStop == -1 and current.time() >= self.TrainList[i].TimeTable[0].time():
        			#starting depot to starting station
        					self.TrainList[i].CurrentStopUpdate()
        					self.TrainList[i].CurrentSiteUpdate()
        					self.TrainList[i].ConvertOperationMode()	#F->T
        					self.TrainList[i].isForward = True
        					self.TrainList[i].MeasureDelay(current)
        					self.RecordedTimeTable[i].append("DEPs:"+str(current - timePerStep))
        					self.LineState.state[0].existTrain = True
        			elif self.LineState.state[self.TrainList[i].CurrentSite].isStation and current.time() > self.TrainList[i].TimeTable[self.TrainList[i].CurrentStop*2].time() and current.time() >= (self.TrainList[i].arrive + datetime.timedelta(seconds=30)).time():
        			#deperture from stations in halfway.
        				if self.LineState.state[self.TrainList[i].CurrentSite+1].existTrain == False: #Collision prevention
        					self.TrainList[i].CurrentStopUpdate()
        					self.TrainList[i].isForward = True
        					self.TrainList[i].MeasureDelay(current)
        					self.RecordedTimeTable[i].append("DEPh:"+str(current - timePerStep))

        		elif self.TrainList[i].CurrentStop == self.StationNum-1: #ARRIVE and DEPERTURE at terminal station
        		# ARRIVE
        			if self.TrainList[i].CurrentStop != -1 and current.time() > self.TrainList[i].TimeTable[self.TrainList[i].CurrentStop*2-1].time():
        				self.TrainList[i].isForward = False
        				if not self.TrainList[i].arrivedFinalStop:
        					self.TrainList[i].MeasureDelay(current)
        					self.TrainList[i].arrivedFinalStop = True
        					self.RecordedTimeTable[i].append("ARRt"+str(current - timePerStep))
        		# DEPERTURE
        		#terminal station to end-side depot
        			if current.time() > self.TrainList[i].TimeTable[self.TrainList[i].CurrentStop*2].time():
        				self.LineState.state[self.TrainList[i].CurrentSite].existTrain = False
        				self.TrainList[i].CurrentStopUpdateToDepot()
        				self.TrainList[i].CurrentSiteUpdateToDepot()
        	  			self.TrainList[i].ConvertOperationMode() #T->F
        				self.TrainList[i].isForward = False

        		#move to the next site cell (represents an inter-section)
        		#print self.LineState.state[self.TrainList[i].CurrentSite].segmentationNumber, self.LineState.hopProb[self.LineState.state[self.TrainList[i].CurrentStop].segmentationNumber]
        		if self.TrainList[i].InOperation and self.TrainList[i].isForward and self.TrainList[i].CurrentSite != 999:
        			if self.LineState.state[self.TrainList[i].CurrentSite+1].existTrain == False : #Collision prevention
        				if random.random() <= self.LineState.state[self.TrainList[i].CurrentSite].hopProb: #Probably control
        					self.LineState.state[self.TrainList[i].CurrentSite].existTrain = False
        					self.TrainList[i].CurrentSiteUpdate()
        					self.LineState.state[self.TrainList[i].CurrentSite].existTrain = True
        	#and self.LineState.state[self.TrainList[i].CurrentSite+2].existTrain == False
        	# print current.time(),self.TrainList[26].TrainNum,self.TrainList[26].CurrentStop,self.TrainList[26].CurrentSite,self.TrainList[26].arrive.time(),self.TrainList[26].isForward,self.TrainList[26].InOperation
        	self.LineState.OutputState(current)
        	current += timePerStep
        #MAIN BODY↑↑

    def outputDelaylog(self):
        #
        os.chdir("/Users/ev30112/Dropbox/programming/MasterMetro/MasterMetroViewer/data")
        outputFile = 'delaylog-'+datetime.datetime.now().strftime('%y%m%d-%H%M%S')+'.txt'

        if os.path.exists(outputFile):
        	f = open(outputFile,'a')
        else:
        	f = open(outputFile,'w')

        for t in TrainList:
        	f.write(str(t.RecordedTime) + '\n')

        f.flush()
        f.close()

    def outputRecordedTimetable(self):
        os.chdir("/Users/ev30112/Dropbox/programming/MasterMetro/MasterMetroViewer/data")
        outputFile = 'RecordedTimeTable-'+datetime.datetime.now().strftime('%y%m%d-%H%M%S')+'.csv'

        if os.path.exists(outputFile):
        	f = open(outputFile,'a')
        else:
        	f = open(outputFile,'w')

        for r in RecordedTimeTable:
        	recorded_row = ""
        	for rw_stmp in r:
        		stmp = rw_stmp.split(" ")[1]
        		recorded_row += str(stmp) + ','
        	f.write(recorded_row[:-1] +'\n')

        f.flush()
        f.close()
