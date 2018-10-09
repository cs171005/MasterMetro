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
		self.arrivedFinalStop = False
		self.arrive = datetime.datetime(100,1,1,4,55,00)
		self.RecordedTime = []

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
		self.RecordedTime.append(currentTime - datetime.timedelta(seconds = 15))
