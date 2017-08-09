# -*- coding: utf-8 -*- 
import csv
import datetime
from CiteCell import *

CellNumPerMinute = 7

list = []
f = open('timetable(interval5).csv', 'rU')

reader = csv.reader(f)
for row in reader:
    list.append(row)
f.close()

for train in list:
	for time in train:
	    print time
	print '--------'

StationNum = 19
interStationMinutes = 3

LineState = []
LineState.append(CiteCell(True,0,False))
for i in range(1,StationNum):
	for j in range(0,interStationMinutes*CellNumPerMinute):
		LineState.append(CiteCell(False,0,False))
	LineState.append(CiteCell(True,0,False))	

current = datetime.datetime(100,1,1,4,50,00)
timePerStep = datetime.timedelta(seconds=60/CellNumPerMinute) 
end = datetime.datetime(100,1,1,14,00,00)

while current <= end:
	print current.time()
	current += timePerStep
	

for cell in LineState:
	print cell.isStation




