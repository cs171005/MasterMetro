# -*- coding: utf-8 -*-
import datetime

class Train:
	def __init__(self,TrainNum,TimeTable):
		self.TrainNum = TrainNum
		self.TimeTable = TimeTable
		self.InOperation = False
		self.isForward = False
		self.CurrentStop = -1
		self.CurrentSite = -1
		self.arrive = datetime.datetime(100,1,1,4,55,00)
		self.delaySecList = []

	def arriveUpdate(self,current):
		self.arrive = current

	def CurrentStopUpdate(self):
		self.CurrentStop += 1

	def CurrentStopUpdateToDepot(self):
		self.CurrentStop = 999

	def CurrentSiteUpdate(self):
		self.CurrentSite += 1

	def CurrentSiteUpdateToDepot(self):
		self.CurrentStop = 999

	def ConvertOperationMode(self):
		self.InOperation = not self.InOperation

	def MeasureDelay(self,currentTime):
		delay = currentTime - self.TimeTable[self.CurrentStop*2-1]
		self.delaySecList.append(delay.seconds - datetime.timedelta(seconds = 15).seconds)
