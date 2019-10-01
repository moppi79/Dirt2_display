import getopt, math, random, sys, time, types, wx, json, struct, socket

from multiprocessing import Process, Queue, cpu_count, current_process, freeze_support

import os


def udp_control (que_out,que_in,target):

	host = "127.0.0.1"
	port = 20777
	print ('UDP start')
	f = open ('data.bin','r')
	a = json.loads(f.read())
	ready= {}
	for c in a:
		ready[c] = bytes.fromhex(a[c]) # return hex to bin
		
	#print (ready)
	looper = 0 #for Psydo data
	
	steering = 0
	#print (inhalt)
	while True:
		time.sleep(0.04)
		looper += 1
		if looper >=499:
			looper = 0
		#print('UDP_MAIN')
		#print (steering)
		if que_in.empty() != True:
			print ('Steering OVERRIDE')
			steering = que_in.get()
		
		
		if  steering == 1:
			looper += 1
			#print ('send data_UDP')
			#print(byte_to_float(ready[str(looper)]))
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			#############ock.connect((host,port))
			sock.bind((host,port))
			
			(aa,ss),a = (sock.recvfrom(300),(host,port))
			hh = byte_to_float(aa)
			#hh = byte_to_float(ready[str(looper)])
			
			target.put(hh)#Retrun data
		elif steering == 'off':
			#print ('UDP Close')
			que_out.put('ok')
			break
		   
def byte_to_float (data):
		stop =  len(data)
		#print (stop)
		data1 = struct.unpack('64f', data[0:256])
		#print (data1)
		couunt = 1
		ausgabe = {}
		for x in data1:
			ausgabe[couunt] = x
			couunt += 1
		
		#print (ausgabe) 
		return(ausgabe)
		'''
		start = 0
		couunt = 1
		ausgabe = {}
		while start <= stop:
			goal = start + 8
			#print (len(data[start:goal]))
			#print (data[start:goal])
			if len(data[start:goal]) == 8:
				aa = struct.unpack('<q',data[start:goal]) # Deltete Tupple
				#print (aa[0])
				#ausgabe[couunt] = struct.unpack('<f',data[start:goal])
				ausgabe[couunt] = aa[0] #Return Float data
			start = goal + 1
			couunt += 1
			
		return(ausgabe)
		'''