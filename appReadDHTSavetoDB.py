import time
import sqlite3
import Adafruit_DHT

dbname='tempDB.db'
sampleFreq = 1*60 # time in seconds ==> Sample each 1 min

# get data from DHT sensor
def getDHTdata(DHTpin):	
	DHT11Sensor = Adafruit_DHT.DHT11
	hum, temp = Adafruit_DHT.read_retry(DHT11Sensor, DHTpin)
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum

# log sensor data on database
def logData (temp, hum, zonecode, zonename):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO sensorSdata values(strftime('%Y-%m-%d','now'),strftime('%H:%M:%S','now'), (?), (?), (?), (?))", (zonecode,zonename,temp,hum))
	conn.commit()
	conn.close()

# main function
def main():
	mySensors={"17":"CUCINA","27":"SOGGIORNO"}
	while True:
		for sensor in mySensors:
			temp, hum = getDHTdata(sensor)
			print(temp,hum, sensor,mySensors[sensor])
			logData (temp, hum,sensor,mySensors[sensor])
			print(sensor)
		time.sleep(sampleFreq)

# ------------ Execute program 
main()
