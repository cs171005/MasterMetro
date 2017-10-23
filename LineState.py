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
		self.hopProbDic = {
		datetime.datetime(100,1,1,8,30,00):[1, 1, 1, 1, 1, 0.3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		datetime.datetime(100,1,1,9,00,00):[1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #Incident
		datetime.datetime(100,1,1,9,15,00):[1, 1, 1, 1, 1, 1, 1, 0.3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		datetime.datetime(100,1,1,10,30,00):[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.3, 1, 1, 1, 1, 1, 1, 1]
		}

	def append(self,newSite):
		self.state.append(newSite)

	def setHopProb(self,current):
		nextApply = datetime.datetime(100,1,1,0,00,00)
		for key in self.hopProbDic.keys():
	 		if key == current:
				self.hopProb = self.hopProbDic[key]
				for site in self.state:
					site.siteHopProbUpdate(self.hopProb)
				break
		# if current >= datetime.datetime(100,1,1,8,30,00):
		# 	self.hopProb = self.hopProbDic[datetime.datetime(100,1,1,8,30,00)]
		# 	for site in self.state:
		# 		site.siteHopProbUpdate(self.hopProbDic[datetime.datetime(100,1,1,8,30,00)])
		# 	# print self.hopProb

	def setHopProbInOneSegment(self,segment,prob):
		newHopProb = self.hopProb
		newHopProb[segment] = prob
		for site in self.state:
			site.siteHopProbUpdate(newHopProb)
		# print self.hopProb

	def setHopProbDic(self,startTime,probArray):
		self.hopProbDic[startTime] = probArray

	def printState(self,currentTime):
		output = ''
		for Site in self.state:
			if Site.isStation:
				output += '['
			if Site.existTrain:
				output += '■'
			else:
				output += '□'
			if Site.isStation:
				output += ']'
		print currentTime.time(),output

	def OutputState(self,currentTime):
		#self.outputFile = 'output'+'.txt'
		os.chdir("/Users/ev30112/Dropbox/programming/MasterMetro/MasterMetroViewer/data")
		self.outputFile = 'result-'+datetime.datetime.now().strftime('%y%m%d-%H%M%S')+'.txt'

		if os.path.exists(self.outputFile):
			f = open(self.outputFile,'a')
		else:
			f = open(self.outputFile,'w')

		output = ''
		for Site in self.state:
			if Site.isStation:
				output += '['
			if Site.existTrain:
				output += '■'
			else:
				output += '□'
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

	def siteHopProbUpdate(self,HPArray):
		if not self.isStation:
			self.hopProb = HPArray[self.segmentationNumber]
