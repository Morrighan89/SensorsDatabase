
import Adafruit_DHT
DHT11Sensor = Adafruit_DHT.DHT11
DHTpin = 17
humidity, temperature = Adafruit_DHT.read_retry(DHT11Sensor, DHTpin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
DHTpin = 27
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')