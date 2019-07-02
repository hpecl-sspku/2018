# -*- coding: utf-8 -*-
# !/usr/bin/python
import sqlite3
import time
import serial
import binascii
import RPi.GPIO as GPIO
from sakshat import SAKSHAT
import threading
import os
GPIO.setmode(GPIO.BCM)

DS = 6
SHCP = 19
STCP = 13
PIN_NO_BEEP = 12
# 开机
ac_open = ['FD','FD','30','03','40','17','00','34','1F','01','2F','02','6A','00','25','00','21','00','27','00','16','05','27','00','2F','0A','27','00','00','00','23','00','FF','FF','FF','FF','FF','FF','FF','FF','01','22','12','22','22','12','12','22','22','22','22','12','22','22','21','21','22','12','32','22','21','22','22','22','22','12','22','22','22','22','22','22','22','22','24','01','22','12','22','22','12','12','22','22','22','22','12','22','22','21','11','22','12','32','22','22','22','22','22','22','22','22','22','22','22','22','22','21','21','15','00','00','F0','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','01','76','3F','A1','DF','DF']
# 关机
ac_close = ['FD','FD','30','03','40','17','00','34','23','01','29','02','68','00','28','00','21','00','27','00','15','05','27','00','2D','0A','28','00','00','00','24','00','FF','FF','FF','FF','FF','FF','FF','FF','01','22','22','22','22','12','12','22','22','22','22','12','22','22','21','21','22','12','32','22','21','22','22','22','22','12','22','22','22','22','22','22','22','22','14','01','22','22','22','22','12','12','22','22','22','22','12','22','22','21','11','22','12','32','22','22','22','22','22','22','22','22','22','22','22','22','22','21','21','25','00','00','F0','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','76','00','7F','DF','DF']
# 温度减：
ac_down = ['FD','FD','30','03','40','17','00','34','24','01','2B','02','23','00','25','00','6A','00','25','00','17','05','26','00','32','0A','27','00','00','00','23','00','FF','FF','FF','FF','FF','FF','FF','FF','01','12','21','11','11','21','11','11','11','11','11','21','11','11','12','12','11','21','31','11','12','11','11','11','11','21','11','11','11','11','11','11','12','21','24','01','12','21','11','11','21','11','11','11','11','11','21','11','11','12','22','11','21','31','11','11','11','11','11','11','11','11','11','11','11','11','11','11','11','25','00','00','F0','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','08','76','01','BB','DF','DF']
# 温度加：
ac_up = ['FD','FD','30','03','40','17','00','34','23','01','2B','02','23','00','26','00','6A','00','25','00','17','05','25','00','33','0A','27','00','00','00','23','00','FF','FF','FF','FF','FF','FF','FF','FF','01','12','21','11','11','12','11','11','11','11','11','21','11','11','12','12','11','21','31','11','12','11','11','11','11','21','11','11','11','11','11','11','12','12','24','01','12','21','11','11','12','11','11','11','11','11','21','11','11','12','22','11','21','31','11','11','11','11','11','11','11','11','11','11','11','11','11','11','21','25','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','EA','DF','DF']
# 制冷：
ac_cold = ['FD','FD','30','03','40','17','00','34','20','01','2D','02','69','00','25','00','22','00','27','00','17','05','27','00','32','0A','26','00','26','01','2C','02','00','00','23','00','FF','FF','FF','FF','01','22','12','22','22','12','12','22','22','22','22','12','22','22','21','21','22','12','32','22','21','22','22','22','22','12','22','22','22','22','22','22','22','22','24','51','22','12','22','22','12','12','22','22','22','22','12','22','22','21','11','22','12','32','22','22','22','22','22','22','22','22','22','22','22','22','22','21','21','16','00','00','F0','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','04','76','3E','8E','DF','DF']
# 制热：
ac_warm = ['FD','FD','30','03','FF','00','00','3F','46','01','D1','08','43','00','09','00','88','00','0B','00','37','05','0B','00','5C','0C','0C','00','3D','01','10','00','18','01','0C','00','3C','00','11','00','01','12','21','11','11','12','11','11','11','11','11','21','11','11','12','12','11','21','31','11','12','11','11','11','11','21','11','11','11','11','11','11','12','12','24','51','12','21','11','11','12','11','11','11','11','11','21','11','11','12','67','70','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','07','00','04','76','01','B8','DF','DF']
# 投影仪：
projector = ['FD','FD','30','03','62','87','00','34','21','01','24','02','68','00','23','00','20','00','23','00','69','0A','24','00','22','01','25','02','33','00','11','00','7B','00','11','00','00','00','0F','00','01','12','22','22','11','21','21','21','22','22','21','22','11','11','12','11','23','41','12','22','22','11','21','21','21','22','22','21','52','16','66','65','66','57','F0','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','30','DF','DF']


def init():
    GPIO.setup(DS, GPIO.OUT)
    GPIO.setup(SHCP, GPIO.OUT)
    GPIO.setup(STCP, GPIO.OUT)

    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.LOW)


def writeBit(data):
    GPIO.output(DS, data)

    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(SHCP, GPIO.HIGH)


# 写入8位LED的状态
def writeByte(data):
    for i in range(0, 8):
        writeBit((data >> i) & 0x01)
    # 状态刷新信号
    GPIO.output(STCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.HIGH)


# 单次哔声
def beep(seconds):
    GPIO.output(PIN_NO_BEEP, GPIO.LOW)
    time.sleep(seconds)
    GPIO.output(PIN_NO_BEEP, GPIO.HIGH)

def send(send_data):
    if (ser.isOpen()):
        #ser.write(send_data.encode('utf-8'))  #utf-8 编码发送
        ser.write(binascii.a2b_hex(send_data))  #Hex发送
        #print("发送成功",send_data)
    else:
        print("send failed")
        
#每5秒执行一次
def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec

# the lightloop threading

def lightLoop():
    while True:
        for i in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]:
            writeByte(i)
            time.sleep(0.1)
            global STOP_FLAG
            if STOP_FLAG:
                break

def smartmode():
    # conn = sqlite3.connect('/home/pi/Smarthome/Smarthome/db.sqlite3')
    # c = conn.cursor()
    # print ("Smartmode opened database successfulliy")
    while True:
        global AUTOFLAG
        if not AUTOFLAG:
            continue
        t = SAKS.ds18b20.temperature
        print(t)
        # input the nodedata
        result = os.popen('/home/pi/smarthome/neural_network/SmartHome {} 50'.format(int(t)))
        res = result.read()
        # close ac
        if '0' in res:
            print('neural network decision close ac')
            for i in range(len(ac_close)):
                send(ac_close[i])
                # 空调关闭
            SAKS.ledrow.off_for_index(0)
        # coldmode
        if '1' in res:
            print('neural network decision code mode')
            for i in range(len(ac_cold)):
                send(ac_cold[i])
        # warmmode
        if '2' in res:
            print('neural network decision warm code')
            for i in range(len(ac_warm)):
                send(ac_warm[i])

        # Repeat every 5 minute 
        time.sleep(10)

        # slots = ''
        # c.execute("UPDATE myhome_commands SET INTENT=?,SLOTS=? where ID=1",(op,slots))
        # conn.commit()
        # conn.close()



def main():
    str1 = '0'
    str2 = '0'
    t1 = threading.Thread(target=lightLoop)
    t2 = threading.Thread(target=smartmode)
    t1.start()
    t2.start()

    while True:
        time.sleep(sleeptime(0,0,2))
        #宣告字符串初始变量为0

        # 连接或创建数据库
        conn = sqlite3.connect('../web_ui/db.sqlite3')
        c = conn.cursor()
        print ("Opened database successfully")

        # 创建表
        #c.execute('create table myhome_commands (id Integer primary key autoincrement , intent Text , slots Text)')
        #print ("create myhome_commands table success")
        #conn.commit()

        # #写入假data
        # c.execute("INSERT INTO myhome_commands (intent,slots) \
        #         VALUES ('INTENT_ERROR', '' )")
        # conn.commit()
        # print ("Records created successfully")

        # 读取sqlite数据库data
        cursor = c.execute("SELECT intent, slots from myhome_commands")
        for row in cursor:
            payload = '{"intent":"%s","slots":"%s","slaveID":3,"control":1,"command_first_byte":1,"command_second_byte":2,"command_third_byte":3,"command_fourth_byte":4}' \
            %(row[0], row[1])

            # 判断读取到的字符串是否有变换（语音控制的输出）
            if str1 in row[0]:
                if str2 in row[1]:
                    print('not new command')
                    break
                else:
                    print('new command')
                    str1 = row[0]
                    str2 = row[1]
            else:
                print('new command')
                str1 = row[0]
                str2 = row[1]
            print (payload)
            if row[0]== 'AC_OPEN' and row[1] == '':
                print("open ac")
                for i in range(len(ac_open)):
                    send(ac_open[i])
                    # 空调打开指示灯
                SAKS.ledrow.on_for_index(0)
                    
            elif row[0]== 'AC_CLOSE' and row[1] == '':
                print('close ac')
                for i in range(len(ac_close)):
                    send(ac_close[i])
                    # 空调关闭
                SAKS.ledrow.off_for_index(0)

            elif row[0]== 'AC_COLD' and row[1] == '':
                print('code mode')
                for i in range(len(ac_cold)):
                    send(ac_cold[i])
            elif row[0]== 'AC_WARM' and row[1] == '':
                print('warm code')
                for i in range(len(ac_warm)):
                    send(ac_warm[i])
            elif row[0]== 'AC_DOWN' and row[1] == '':
                print('lower tem')
                for i in range(len(ac_down)):
                    send(ac_down[i])

            elif row[0]== 'AC_UP' and row[1] == '':
                print('higher tem')
                for i in range(len(ac_up)):
                    send(ac_up[i])

            elif row[0]== 'OPEN_PPT' and row[1] == '':
                print('open projector')
                for i in range(len(projector)):
                    send(projector[i])
                    # 投影仪打开指示灯
                SAKS.ledrow.on_for_index(1)

            elif row[0]== 'CLOSE_PPT' and row[1] == '':
                print('close projector')
                for i in range(len(projector)):
                    send(projector[i])
                    # 投影仪关闭
                SAKS.ledrow.off_for_index(1)

            elif row[0]== 'OPEN_BOX' and row[1] == '':
                print('open audio')
                # 音响开
                global STOP_FLAG
                STOP_FLAG = False

            elif row[0]== 'CLOSE_BOX' and row[1] == '':
                # global STOP_FLAG
                STOP_FLAG = True
                print('close audio')
                # 音响关
                writeByte(0x00) 

            elif row[0] == 'AUTOMODE' and row[1] == '':
                print('smart mode')
                global AUTOFLAG
                AUTOFLAG = True

            elif row[0] == 'NORMALMODE' and row[1] == '':
                print('normal mode')
                # global AUTOFLAG
                AUTOFLAG = False

            elif row[0]== 'INTENT_ERROR' and row[1] == '':
                print('INTENT ERROR')
                # 蜂鸣器警告
                beep(0.05)

        #温度显示
        temp = SAKS.ds18b20.temperature
        SAKS.digital_display.show(("%.2f" % temp).replace(' ','#'))

        # #创建表
        # c.execute('create table myhome_nodedata (id Integer primary key autoincrement , time Text , localshortaddr Text , gateway_id Text , slaveId Text , humidity Integer , temperature Integer , light Integer , noise Integer , co2_simulation Integer , co2_binarization Integer)')
        # print ("create myhome_nodedata table success")
        # conn.commit()

        #写入data
        sql = "insert into myhome_nodedata(time,localshortaddr, gateway_id,slaveId, humidity, temperature,light, noise, co2_simulation, co2_binarization)values('%s','%s','%s','%s',%f,%f,%f,%f,%f,%f)" % (0,0,0,0,63.2, temp,862.13,77.61,0.14,0.14)
        conn.execute(sql)
        conn.commit()
        print ("Records created successfully insert into myhome_nodedata values")
        #beep(0.05)
        print ("Operation done successfully")
        conn.close()

if __name__ == '__main__':
    STOP_FLAG = True
    AUTOFLAG = False
    try:

        SAKS = SAKSHAT()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_NO_BEEP, GPIO.OUT, initial=GPIO.HIGH)
        ser = serial.Serial('/dev/ttyAMA0',9600)
        if(ser.isOpen()):
            print("open serial successful")
        else:
            print("open serial failed")
        init()



        while True:
            main()
            
    except KeyboardInterrupt:
        print("except")
        #LED组全关
        writeByte(0x00)
        GPIO.cleanup()

