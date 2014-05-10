import serial
import logging	

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)

readings = []
logging.basicConfig(format='%(asctime)s %(levelname)s [%(funcName)s] (%(module)s:%(lineno)d) - %(message)s',level=logging.DEBUG)
data = bytearray()
while True :
	tmp = ser.read(1)
	data.append(tmp)
	#leggo un tot numero di record e poi esco
	if(len(readings)==300):
		break
	#se trovo un fine linea scrivo il dato nell'array
	if(tmp == '\r'):
		data = data[1:-1]
		data = int(data.decode(encoding='ASCII').encode(encoding='ASCII'))
		logging.debug("data ->%s<-",data)
		readings.append(data)		
		data = bytearray()
ser.close()	
readings.sort()
logging.info("readings %s",readings)