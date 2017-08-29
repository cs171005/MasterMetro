# -*- coding: utf-8 -*- 
import os.path
import os
import datetime

class LineState:
	def __init__(self):
		self.state = []
		self.outputFile = ''
	
	def append(self,newSite):
		self.state.append(newSite)
	
	def printState(self,currentTime):
		output = ''
		for Site in self.state:
			if Site.isStation:
				output += '['
			if Site.existTrain:
				output += '1'
			else:
				output += '0'
			if Site.isStation:
				output += ']'
		print currentTime.time(),output
	
	def OutputState(self,currentTime):
		self.outputFile = 'output'+datetime.datetime.now().strftime('%s')+'.txt'
		if os.path.exists(self.outputFile):
			f = open(self.outputFile,'a')
		else:
			f = open(self.outputFile,'w')
		
		output = ''
		for Site in self.state:
			if Site.isStation:
				output += '['
			if Site.existTrain:
				output += '1'
			else:
				output += '0'
			if Site.isStation:
				output += ']'
		f.write(str(currentTime.time())+' '+output+'\n')
		f.flush()
		f.close()
		
 
		
class SiteCell:
    
	def __init__(self,isStation,segmentationNumber,stationNumber,existTrain):
		self.existTrain = existTrain
		self.segmentationNumber = segmentationNumber
		self.isStation = isStation
		self.stationNumber = stationNumber
