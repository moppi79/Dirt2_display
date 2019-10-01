import getopt, math, random, sys, time, types, wx, json, struct

from multiprocessing import Process, Queue, cpu_count, current_process, freeze_support


import os
import wx





def dispatcher (wxin,wxout,udpin,udpout):
	print ('Dispatcher start')
	off_on = 0 
	number = 0 
		
	while True:
		#print ('Dispatcher_MAIN')
		#print (off_on)
		time.sleep(0.02) 
		if wxin.empty() != True:
			#print ('NEW STEERING DISPATCHER')
			d = wxin.get()
			#Print (d)
			if d == 1: 
				udpout.put(1)
				off_on = 1
			elif d == 'off':
				off_on = 0
				udpout.put('off')
				while True:
					print ('Dispatcher on hold')
					time.sleep(0.1)
					if udpin.empty() != True:
						
						if udpin.get() == 'ok':
							print ('Dispatcher Close')
							wxout.put('ok')
							break
								  
				print ('Dispatcher Close Finally ')
				break
			elif d == 0:
				print ('off_Dispatcher_main') 
				off_on = 0
				udpout.put(0)
				
		if off_on == 1:
			#print ('send data_DISPATCHER_BEGIN')
			if udpin.empty() != True:
				#print ('send data_DISPATCHER')
				ass = udpin.get()
				#print (ass)
				wxout.put(ass)
