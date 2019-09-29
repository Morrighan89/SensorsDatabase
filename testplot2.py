import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as dat
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import sqlite3
from dateutil import tz




def getHistData (numSamples=43000,location="*",stDate=dt.datetime.utcnow()+dt.timedelta(hours=-23),endDate=dt.datetime.utcnow()):
	print(location)
	#if stDate.hour<=endDate.hour:
	#	curs.execute("SELECT * FROM sensorsData WHERE tdata >= (?) and tdata <= (?) and ttime >= (?) and ttime < (?) and zonename = (?) ORDER BY   tdata DESC , ttime DESC LIMIT (?)",(dt.datetime.strftime(stDate,'%Y-%m-%d'),dt.datetime.strftime(endDate,'%Y-%m-%d'),dt.datetime.strftime(stDate,'%H:%M:%S'),dt.datetime.strftime(endDate,'%H:%M:%S'),location, numSamples))
	#else:
	#	curs.execute("SELECT * FROM sensorsData WHERE tdata >= (?) and tdata <= (?) and (ttime <= (?) or ttime >= (?)) and zonename = (?) ORDER BY   tdata DESC , ttime DESC LIMIT (?)",(dt.datetime.strftime(stDate,'%Y-%m-%d'),dt.datetime.strftime(endDate,'%Y-%m-%d'),dt.datetime.strftime(stDate,'%H:%M:%S'),dt.datetime.strftime(endDate,'%H:%M:%S'),location, numSamples))
	print(stDate,endDate,dt.datetime.strftime(stDate,'%H:%M:%S'),dt.datetime.strftime(stDate,'%Y-%m-%d'))
	#curs.execute("SELECT * FROM sensorsData WHERE tdata >= (?) and tdata <= (?) and ttime >= (?) and ttime < (?)) and zonename = (?) ORDER BY   tdata DESC , ttime DESC LIMIT (?)",(dt.datetime.strftime(stDate,'%Y-%m-%d'),dt.datetime.strftime(endDate,'%Y-%m-%d'),dt.datetime.strftime(stDate,'%H:%M:%S'),dt.datetime.strftime(endDate,'%H:%M:%S'),location, numSamples))
	curs.execute("SELECT * FROM sensorsData WHERE tdata >= (?) and tdata <= (?)  and zonename = (?) ORDER BY   tdata DESC , ttime DESC LIMIT (?)",(dt.datetime.strftime(stDate,'%Y-%m-%d'),dt.datetime.strftime(endDate,'%Y-%m-%d'),location, numSamples))

	data = curs.fetchall()
	#dates = []
	timeStamps = []
	temps = []
	hums = []
	#from_zone = tz.gettz('Europe/Rome')
	#to_zone = tz.gettz('UTC')
	for row in reversed(data):
		#print(row[0],row[1])
		timeStamp=dt.datetime.strptime(row[0]+row[1], '%Y-%m-%d%H:%M:%S')
		if timeStamp>stDate and timeStamp<endDate:
			timeStamp=datetime_from_utc_to_local(timeStamp)
			
			timeStamps.append(timeStamp)
			temps.append(row[4])
			hums.append(row[5])
	return timeStamps, temps, hums

def plot_temp():
	timeStamps, temps, hums = getHistData(numSamples,location)
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

def plot_hum():
	timeStamps, temps, hums = getHistData(numSamples,location)

	ys = hums
	xs = timeStamps
	formatter = dat.DateFormatter('%d-%m %H:%M')
	fig = Figure()
	ax = fig.add_subplot(1, 1, 1)
	
	output = io.BytesIO()
	#canvas.print_png(output)
	#response = make_response(output.getvalue())
	#response.mimetype = 'image/png'
	#return response
	#fig, ax = plt.subplots()
	ax.set_title("Humidity [%]")
	ax.grid(True)
	ax.plot_date(xs, ys,'o-')
	#ax.xaxis.set_major_locator(loc)
	ax.xaxis.set_major_formatter(formatter)
	ax.xaxis.set_tick_params(rotation=30, labelsize=10)
	fig.autofmt_xdate()
	fig.tight_layout()
	canvas = FigureCanvas(fig)
	canvas.print_figure('test')
	#plt.show()


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = dt.datetime.fromtimestamp(now_timestamp) - dt.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset
	
conn=sqlite3.connect('tempDB.db')
curs=conn.cursor()
numSamples = 15000
location="SOGGIORNO"
plot_hum()
plot_temp()
# Create figure for plotting
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#xs = []
#ys = []
