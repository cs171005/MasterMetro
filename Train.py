# -*- coding: utf-8 -*- 

class Train:
	def __init__(self,TrainNum,TimeTable):
		self.TrainNum = TrainNum
		self.TimeTable = TimeTable
		self.InOperation = False		
		self.CurrentStop = -1
		self.CurrentSite = -1
	
	def CurrentStopUpdate(self):
		self.CurrentStop += 1
	
	def CurrentStopUpdateToDepot(self):
		self.CurrentStop = 999
	
	def CurrentSiteUpdate(self):
		self.CurrentSite += 1
	
	def ConvertOperationMode(self):
		self.InOperation = not self.InOperation
		