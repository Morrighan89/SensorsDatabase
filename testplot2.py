import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as dat
import sqlite3
from dateutil import tz




def getHistData (numSamples,location,stDate=dt.datetime.utcnow()+dt.timedelta(hours=-9),endDate=dt.datetime.utcnow()):
	#print(location)
	#print(stDate,dt.datetime.strftime(stDate,'%H:%M:%S'),dt.datetime.strftime(stDate,'%Y-%m-%d'))
	curs.execute("SELECT * FROM sensorsData WHERE tdata >= (?)  AND tdata <= (?) and ttime >= (?) and ttime < (?) and zonename = (?) ORDER BY   tdata DESC, ttime DESC LIMIT (?) ",(dt.datetime.strftime(stDate,'%Y-%m-%d'),dt.datetime.strftime(endDate,'%Y-%m-%d'),dt.datetime.strftime(stDate,'%H:%M:%S'),dt.datetime.strftime(endDate,'%H:%M:%S'),location,str(numSamples)))
	#curs.execute("SELECT * FROM sensorsData WHERE tdata >= (?) and zonename = (?) ORDER BY   tdata DESC, ttime ",(dt.datetime.strftime(stDate,'%Y-%m-%d'),location))

	data = curs.fetchall()
	#dates = []
	timeStamps = []
	temps = []
	hums = []
	#from_zone = tz.gettz('Europe/Rome')
	#to_zone = tz.gettz('UTC')
	for row in reversed(data):
		print(row[0],row[1])
		timeStamp=dt.datetime.strptime(row[0]+row[1], '%Y-%m-%d%H:%M:%S')

		timeStamp=datetime_from_utc_to_local(timeStamp)
		
		timeStamps.append(timeStamp)
		temps.append(row[4])
		hums.append(row[5])
	return timeStamps, temps, hums

#def plot_temp():
#	timeStamps, temps, hums = getHistData(numSamples,location)
#	ys = temps
#	fig = Figure()
#	axis = fig.add_subplot(1, 1, 1)
#	axis.set_title("Temperature [°C]")
#	axis.set_xlabel("Samples")
#	axis.grid(True)
#	xs = range(numSamples)
#	axis.plot(xs, ys)
#	canvas = FigureCanvas(fig)
#	output = io.BytesIO()
#	canvas.print_png(output)
#	response = make_response(output.getvalue())
#	response.mimetype = 'image/png'
#	return response

def plot_hum():
	timeStamps, temps, hums = getHistData(numSamples,location)

	ys = hums
	#ys= temps
	xs = timeStamps
	formatter = dat.DateFormatter('%d-%m %H:%M')
	#fig = Figure()
	#axis = fig.add_subplot(1, 1, 1)
	#canvas = FigureCanvas(fig)
	#output = io.BytesIO()
	#canvas.print_png(output)
	#response = make_response(output.getvalue())
	#response.mimetype = 'image/png'
	#return response
	fig, ax = plt.subplots()
	ax.set_title("Humidity [%]")
	ax.grid(True)
	plt.plot_date(xs, ys,'o-')
	#ax.xaxis.set_major_locator(loc)
	ax.xaxis.set_major_formatter(formatter)
	ax.xaxis.set_tick_params(rotation=30, labelsize=10)

	plt.show()


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = dt.datetime.fromtimestamp(now_timestamp) - dt.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset
	
conn=sqlite3.connect('tempDB.db')
curs=conn.cursor()
numSamples = 15000
location="SOGGIORNO"
plot_hum()
# Create figure for plotting
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#xs = []
#ys = []
