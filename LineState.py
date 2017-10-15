# -*- coding: utf-8 -*-
import os.path
import os
import datetime
# from main import StationNum
class LineState:
	def __init__(self):
		self.state = []
		self.outputFile = ''
		self.hopProb = [1]*19 #StationNum #default:trains always progress.

	def append(self,newSite):
		self.state.append(newSite)

	def setHopProb(self,segmentation,prob):
		self.hopProb[segmentation] = prob

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
		#self.outputFile = 'output'+'.txt'
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
		self.hopProb = 1 #default:1

	def hopProbUpdate(self,HPArray):
		if not self.isStation:
			self.hopProb = HPArray[self.segmentationNumber]
