#!/usr/bin/env python


'''
Tool to create flash dump via serial connection to a uboot with command "nand dump".
'''


import serial
import time
import sys
import os

def rsp2ba(response):
    if len(response) < 6700:
        raise Exception('too short input to rsp2ba')
    prefix = 'dump:'
    postfix = 'OOB:'
    startidx = response.find(prefix) + len(prefix) 
    endidx = response.find(postfix)
    if startidx == -1 or endidx == -1:
        raise Exception('invalid input to rsp2ba') 
    stripped_ascii = response[startidx:endidx]
    databytes = bytearray.fromhex( stripped_ascii)
    return databytes

def serialCmdRsp(ser, cmd):
    ser.readall()
    ser.write(cmd.encode())
    time.sleep(0.9)
    rsp = ser.readall()
    return rsp.decode()

def printprogress(p):
    print(p, end='\r')

if len(sys.argv) != 4:
    raise Exception('need 3 arguments: <filename> <start page> <nr of pages>')

filename = sys.argv[1]
startpage = int(sys.argv[2])
nrpages = int(sys.argv[3])
print("filename:", filename)
print("start page:", startpage)
print("nr pages:", nrpages)

if os.path.exists(filename):
    raise Exception('error file ' + filename + ' already exists') 
 
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)
ser.readall()

f=open(filename, 'wb') 

for p in range(startpage,startpage+nrpages):
    printprogress(p)
    byteaddress = 2048*p
    hexaddr = hex(byteaddress)
    cmdstr = 'nand dump ' + hexaddr + '\n'
    try:
        resp = serialCmdRsp(ser, cmdstr)
    except SerialException:
        print("serialexception")
        print("current page:", p) 
        raise Exception("exiting because of serial exception")  
    parsedresp = rsp2ba(resp)
    f.write(parsedresp)

f.close()

