import os
import sqlite3
import time

#result = os.system('/home/pi/ksq/SmartHome 33 50')
conn = sqlite3.connect('/home/pi/Smarthome/Smarthome/db.sqlite3')
c = conn.cursor()
print ("Opened database successfulliy")

# TODO: read the tempreture data
# input the nodedata
result = os.popen('/home/pi/Smarthome/Smarthome/neural_network/SmartHome 13 50')

res = result.read()

#if res.find("2"):
#    print (res)
    
#print (res)  
#print(type(res))
op = 'INTENT_ERROR'
if '0' in res:
    print (res)
    op = 'AC_CLOSE'
if '1' in res:
    print (res)
    op = 'AC_COLD'
if '2' in res:
    print (res)
    op = 'AC_WARM'

slots = ''
# sql = "insert into myhome_nodedata(time,localshortaddr, gateway_id,slaveId, humidity, temperature,light, noise, co2_simulation, co2_binarization)values('%s','%s','%s','%s',%f,%f,%f,%f,%f,%f)" % (time.strftime('%Y-%m-%d/%H:%M:%S'),"F5A1","0","1",50,13,0,0,0,op)
c.execute("UPDATE myhome_commands SET INTENT=?,SLOTS=? where ID=1",(op,slots))
conn.commit()
conn.close()
# print ("Records created successfully insert into myhome_nodedata values")
# sql = "select * from myhome_nodedata"
# c.execute(sql)
#sql = "select * from myhome_nodedata where id=?"
# sql = "select * from myhome_nodedata order by id desc limit 0,50"

#c.execute(sql,("510",))
#c.execute(sql)

# values = c.fetchall()
# print(values)
# c.close()


#order = '/home/pi/ksq/SmartHome 33 50'
#pi= subprocess.Popen(order,shell=True,stdout=subprocess.PIPE)
#print pi.stdout.read()

#output = os.popen('/home/pi/ksq/SmartHome 33 50') 
#(status, output) = subprocess.getstatusoutput('/home/pi/ksq/SmartHome 33 50')


#print (output)  
#print (status)

#print (result)

#print ("123")
