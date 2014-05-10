import serial
import logging	
import io
#ser = serial.Serial("/dev/ttyUSB0", 9600, timeout = 60)
#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)

#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),newline='\r',encoding='ascii')
ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),  
                               newline = '\r',
                               line_buffering = True)

#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), encoding='ascii')
#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser,8))
line = ""
mys = ""
print "qui"
data = bytearray()
while True :
	print "loop"
	#line = sio.readline()[:-1]
	#line = ser.read(64).decode("ascii")
	#line = sio.readline()
	line = ser.readline().decode('ascii')[:-1]
	print line	

ser.close()	
