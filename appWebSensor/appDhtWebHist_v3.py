#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  appDhtWebHist_v2.py
#  
#  Created by MJRoBot.org 
#  10Jan18

'''
	RPi WEb Server for DHT captured data with Gage and Graph plot  
'''

from datetime import datetime
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as dat

from dateutil import tz

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('../tempDB.db', check_same_thread=False)
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
#aggiunger for sensors in sensor slect where u sensor and output data become vectors
	for row in curs.execute("SELECT * FROM sensorsData ORDER BY  ttime desc, tdata desc limit 1"):
		date=str(row[0])
		time = str(row[1])
		temp = row[4]
		hum = row[5]
	#conn.close()
	return date,time, temp, hum

# Get 'x' samples of historical data
def getHistData (numSamples=43000,location="*",stDate=dt.datetime.utcnow()+dt.timedelta(hours=-23),endDate=dt.datetime.utcnow()):
	curs.execute("SELECT * FROM sensorsData WHERE tdata >= (?) and tdata <= (?)  and zonename = (?) ORDER BY   tdata DESC , ttime DESC LIMIT (?)",(dt.datetime.strftime(stDate,'%Y-%m-%d'),dt.datetime.strftime(endDate,'%Y-%m-%d'),location, numSamples))

	data = curs.fetchall()
	timeStamps = []
	temps = []
	hums = []
	for row in reversed(data):
		timeStamp=dt.datetime.strptime(row[0]+row[1], '%Y-%m-%d%H:%M:%S')
		if timeStamp>stDate and timeStamp<endDate:
			timeStamp=datetime_from_utc_to_local(timeStamp)
			
			timeStamps.append(timeStamp)
			temps.append(row[4])
			hums.append(row[5])
	return timeStamps, temps, hums

# Test data for cleanning possible "out of range" values
def testeData(temps, hums):
	n = len(temps)
	for i in range(0, n-1):
		if (temps[i] < -10 or temps[i] >50):
			temps[i] = temps[i-2]
		if (hums[i] < 0 or hums[i] >100):
			hums[i] = temps[i-2]
	return temps, hums


# Get Max number of rows (table size)
def maxRowsTable():
	for row in curs.execute("select COUNT(temperature) from  sensorsData"):
		maxNumberRows=row[0]
	return maxNumberRows

# Get sample frequency in minutes
def freqSample():
	dates, times, temps, hums = getHistData (2)
	fmt = '%Y-%m-%d %H:%M:%S'
	tstamp0 = datetime.strptime(dates[0]+" "+times[0], fmt)
	tstamp1 = datetime.strptime(dates[1]+" "+times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)

# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
        numSamples = 100

global freqSamples
freqSamples = freqSample()

global rangeTime
rangeTime = 100
				
		
# main route 
@app.route("/")
def index():
	date, time, temp, hum = getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'freq'		: freqSamples,
      'rangeTime'		: rangeTime
	}
	return render_template('index_0.3.html', **templateData)

@app.route("/soggiorno.html")
def soggiorno():
	date, time, temp, hum = getHistData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'freq'		: freqSamples,
      'rangeTime'		: rangeTime
	}
	return render_template('soggiorno.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples 
    global freqSamples
    global rangeTime
    rangeTime = int (request.form['rangeTime'])
    if (rangeTime < freqSamples):
        rangeTime = freqSamples + 1
    numSamples = rangeTime//freqSamples
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    
    time, temp, hum = getLastData()
    
    templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'freq'		: freqSamples,
      'rangeTime'	: rangeTime
	}
    return render_template('index.html', **templateData)

@app.route('/soggiorno', methods=['POST'])
def my_form_post():
    global numSamples 
    global freqSamples
    global rangeTime
    global beTime = int (request.form['beTime'])
	global enTime = int (request.form['enTime'])
	
        
    time, temp, hum = getHistData(43000,"SOGGIORNO",beTime,enTime)
    
    templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'freq'		: freqSamples,
      'rangeTime'	: rangeTime
	}
    return render_template('soggiorno.html', **templateData)
	
	
@app.route('/plot/temp')
def plot_temp():
	timeStamps, temps, hums = getHistData(43000,"SOGGIORNO",beTime,enTime)
	formatter = dat.DateFormatter('%d-%m %H:%M')
	ys = temps
	xs=timeStamps
	fig = Figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title("Temperature [°C]")
	ax.xaxis.set_major_formatter(formatter)
	ax.xaxis.set_tick_params(rotation=30, labelsize=10)
	ax.grid(True)
	ax.plot_date(xs, ys,'o-')
	fig.autofmt_xdate()
	fig.tight_layout()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/hum')
def plot_hum():
	timeStamps, temps, hums = getHistData(43000,"SOGGIORNO",beTime,enTime)
	formatter = dat.DateFormatter('%d-%m %H:%M')
	ys = temps
	xs=timeStamps
	fig = Figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title("Humidity [%]")
	ax.xaxis.set_major_formatter(formatter)
	ax.xaxis.set_tick_params(rotation=30, labelsize=10)
	ax.grid(True)
	ax.plot_date(xs, ys,'o-')
	fig.autofmt_xdate()
	fig.tight_layout()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response
	
if __name__ == "__main__":
   app.run()

