# -*- coding: utf-8 -*- 

class Train:
	def __init__(self,TrainNum,TimeTable):
		self.TrainNum = TrainNum
		self.TimeTable = TimeTable
		self.CurrentStop = -1
		self.CurrentSite = -1
	
	def CurrentStopUpdate(self):
		self.CurrentStop += 1
	
	def CurrentStopUpdateToDeposit(self):
		self.CurrentStop = 999
		