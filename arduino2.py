import serial
import logging
import ConfigParser
import time
import datetime
import sqlite3
import MySQLdb

#def di una eccezione per capire se arduino risponde o meno via seriale
class ArduinoTimeout(Exception):
	pass
	
class SerialLockTimeout(Exception):
	pass
	
def listenData(config):	
	"""
	Invia i comandi ad arduino, in base al firmware restituisce gli n valori
	"""
	
	#ser = serial.Serial("/dev/ttyACM0", "9600", timeout = 10)
	ser = serial.Serial("/dev/ttyUSB0", "9600", timeout = 10)
	line = ""
	start_time = time.time()
	count=0
	total_distance = 2240
	db = MySQLdb.connect("localhost", "batch", "batch", "test")
	curs2=db.cursor()
	
	while True:
		line = ser.readline().strip()
		logging.debug(line)
#		if(line.find("wireless")!=-1):
#			continue
		if(line[:5] == "node:"):
#			count = count +1
#			if(count==1):
#				continue
			#aggiorno il timestamp posix corrente
			currtime = int(time.time())
			logging.debug("currtime->%s",currtime)
			tz_offset = time.timezone * -1
			logging.debug("tz_offset->%s",tz_offset)
			currtime = currtime + tz_offset + 3600
			logging.debug("currtime->%s",currtime)
			ser.write("updatetime,"+str(currtime)+",\n")

			tmp1 = line.split(";")
			node = int(tmp1[0].split(":")[1])
			logging.debug("node->%s",node)
			#Data dal sensore ad ultrasuoni
			if(tmp1[0].split(":")[1]=="1"):
				distance = float(tmp1[2].split(":")[1]);
				logging.debug("distance %s",distance)
				distance = total_distance - distance
				conn = sqlite3.connect("/home/pi/test.db")
				curs = conn.cursor()
				curs.execute("replace into snow (station_time,distance) values(?,?)",(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),distance))
				conn.commit()
				conn.close()
			#Data dal sensore umidita/temperatura
			if(tmp1[0].split(":")[1]=="2"):
				humidity = float(tmp1[2].split(":")[1]);
				temperature = float(tmp1[1].split(":")[1]);
				logging.debug("humidity %s",humidity)
				logging.debug("temperature %s",temperature)
				conn = sqlite3.connect("/home/pi/test.db")
				curs = conn.cursor()
				curs.execute("replace into remote_temp (station_time,humidity,temperature) values(?,?,?)",(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),humidity,temperature))
				conn.commit()
				conn.close()
			#Data dal sensore umidita/temperatura
			if(tmp1[0].split(":")[1]=="5"):
				humidity = float(tmp1[3].split(":")[1]);
				temperature = float(tmp1[4].split(":")[1]);
				battery = int(tmp1[5].split(":")[1].strip());
				logging.debug("humidity %s",humidity)
				logging.debug("battery %s",battery)
				logging.debug("temperature %s",temperature)
				#curs2.execute("INSERT INTO sensori_temperatura (temperature,humidity) values(%f,%f)",(temperature,humidity))
				curs2.execute("INSERT INTO sensori_temperatura (temperature,humidity,battery,sensor_id) values(%s,%s,%s,%s)",(temperature,humidity,battery,node))
				db.commit()
				logging.debug("commit")
				
		
	ser.close()

def main():		
	logging.basicConfig(format='%(asctime)s %(levelname)s [%(funcName)s] (%(module)s:%(lineno)d) - %(message)s',level=logging.DEBUG)	
	#config = ConfigParser.ConfigParser()
	#config.read('arduino.cdg')
	listenData("");
	
		
	logging.debug("sensors-> %s",sensors)
	
if __name__ == "__main__":
    main()		
