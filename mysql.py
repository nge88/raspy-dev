
import MySQLdb


db = MySQLdb.connect("localhost", "batch", "batch", "test")
curs=db.cursor()
temperature = 10.5
humidity = 87
curs.execute("INSERT INTO sensori_temperatura (temperature,humidity,sensor_id) values(%s,%s,1)",(temperature,humidity))
db.commit()
print "Data committed"
