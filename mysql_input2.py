import time
import MySQLdb as msdb
import serial
import types
from threading import Thread
db=msdb.connect("localhost","root","","library")
import RPi.GPIO as gpio
import rfidreader1

done=True

def book_reader():
        sql="""CREATE TABLE IF NOT EXISTS rfids(id varchar(10) primary key,row int(3) not null,col int(3) not null,rack int(3) not null)"""
        pin=5
        cur=db.cursor()
        gpio.setmode(gpio.BOARD)
        gpio.setup(pin,gpio.OUT)
        cur.execute(sql)
        res=0

        while True and done:
                gpio.output(pin,gpio.LOW)
                res=rfidreader1.reading()
                print res
                sql="select id from rfids where id='%s' ;"%res
                cur.execute(sql)
                if cur.fetchone() is not None:
                        gpio.output(pin,gpio.HIGH)
                        print "Already exist"
                        u=1;
                        
                        
                elif res!=None:
                        inp=raw_input("Enter the position as: row col rack").strip('\n')
                        inp=inp.split(" ")
                        sql="insert into rfids(id,row,col,rack) values('%s',%s,%s,%s);" %(res,inp[0],inp[1],inp[2])
                        try:
                                gpio.output(pin, gpio.LOW)
                                cur.execute(sql)
                                db.commit()
                        except Exception as e:
                                print "Some error occured:",e
                                u=0;
                                db.rollback()
                else:
                        break
                
                time.sleep(1)

ser=serial.Serial('/dev/ttyACM0',9600)

def position_reader():
        db=msdb.connect("localhost","root","","library")
        sql="""CREATE TABLE IF NOT EXISTS positions(id varchar(10) primary key,xpos int(3) not null,ypos int(3) not null)"""
        curr=db.cursor()
        curr.execute(sql)
        
        while True and done:
                a=ser.readline().strip("\n").strip("\r")
                print a
                sql="select id from positions where id='"+a+"';"
                curr.execute(sql)
                if curr.fetchone() is None:
                        inp=raw_input("Enter the position as x y:").strip('\n')
                        inp=inp.split(" ")
                        sql="insert into positions(id,xpos,ypos) values('%s',%s,%s);" %(a,inp[0],inp[1])
                        try:
                                curr.execute(sql)
                                db.commit()
                                print "Added"
                        except:
                                print "Some Error occured"
                                db.rollback()
                else:
                        print "Already Exists"	


t1=Thread(target=position_reader)
t1.start()
try:
        book_reader()
except:
        done=False
