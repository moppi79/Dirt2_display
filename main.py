import getopt, math, random, sys, time, types, wx, json, struct

from multiprocessing import Process, Queue, cpu_count, current_process, freeze_support
from datetime import datetime

import os
import wx

from UDP_control import *

from Dispatcher import *
from test import test_logging
from _ast import While
from asyncio.tasks import sleep

print (wx.version())

class MainWindow(wx.Frame):
	def __init__(self, parent, title, que_out,que_in):
		self.out_dispatcher = que_out
		self.in_dispatcher = que_in
		self.status_proc = 0
		self.maus = wx.MouseState()
		
		wx.Frame.__init__(self, parent, title=title)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		grid = wx.GridBagSizer(hgap=12, vgap=6) ##HAUPT GRID
		hSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#mainSizer.add(self,CalcMin(1000))
		
		#####GRAFIK LOAD ########
		self.quote = wx.StaticText(self, label="Your quote: ")
		grid.Add(self.quote, pos=(0,0))
		
		self.graf_handles = {}
		loop = 0
		while loop <= 9:
			self.graf_handles[str(loop)+'o'] = wx.Image()
			self.graf_handles[str(loop)+'o'].LoadFile('zahl/'+str(loop)+'.jpg')
			self.graf_handles[str(loop)+'s'] = wx.Image()
			self.graf_handles[str(loop)+'s'].LoadFile('zahl/'+str(loop)+'.jpg')
			self.graf_handles[str(loop)+'g'] = wx.Image()
			self.graf_handles[str(loop)+'g'].LoadFile('zahl/'+str(loop)+'.jpg')
			
			aa =  self.graf_handles[str(loop)+'s'].GetSize()
			s0 = (round((aa[0]/100)*40))
			s1 = (round((aa[1]/100)*40))
			g0 = (round((aa[0]/100)*50))
			g1 = (round((aa[1]/100)*50))
			self.graf_handles[str(loop)+'s'] = self.graf_handles[str(loop)+'s'].Scale(s0,s1)
			self.graf_handles[str(loop)+'g'] = self.graf_handles[str(loop)+'g'].Scale(g0,g1)
			
			loop += 1
		print (self.graf_handles)
		self.graf_handles['gfx_static'] = {}
		self.graf_handles['gfx_static']['0r'] = wx.StaticBitmap(self,wx.ID_ANY,self.graf_handles['0g'].ConvertToBitmap())
		self.graf_handles['gfx_static']['1r'] = wx.StaticBitmap(self,wx.ID_ANY,self.graf_handles['0g'].ConvertToBitmap())
		self.graf_handles['gfx_static']['2r'] = wx.StaticBitmap(self,wx.ID_ANY,self.graf_handles['0g'].ConvertToBitmap())
		self.graf_handles['gfx_static']['3r'] = wx.StaticBitmap(self,wx.ID_ANY,self.graf_handles['0g'].ConvertToBitmap())
		self.graf_handles['gfx_static']['0s'] = wx.StaticBitmap(self,wx.ID_ANY,self.graf_handles['0s'].ConvertToBitmap())
		self.graf_handles['gfx_static']['1s'] = wx.StaticBitmap(self,wx.ID_ANY,self.graf_handles['0s'].ConvertToBitmap())
		self.graf_handles['gfx_static']['2s'] = wx.StaticBitmap(self,wx.ID_ANY,self.graf_handles['0s'].ConvertToBitmap())
		
		self.speedgrid = wx.GridBagSizer(hgap=2, vgap=1)#minigrid KM/H / RPM
		self.kmhgrid = wx.GridBagSizer(hgap=2, vgap=4)
		self.rpmgrid = wx.GridBagSizer(hgap=1, vgap=4)
		self.rpmgrid.Add(self.graf_handles['gfx_static']['0r'], pos=(0,0))
		self.rpmgrid.Add(self.graf_handles['gfx_static']['1r'], pos=(0,1))
		self.rpmgrid.Add(self.graf_handles['gfx_static']['2r'], pos=(0,2))
		self.rpmgrid.Add(self.graf_handles['gfx_static']['3r'], pos=(0,3))
		self.kmhgrid.Add(self.graf_handles['gfx_static']['0s'], pos=(0,0))
		self.kmhgrid.Add(self.graf_handles['gfx_static']['1s'], pos=(0,1))
		self.kmhgrid.Add(self.graf_handles['gfx_static']['2s'], pos=(0,2))
		self.speedgrid.Add(self.kmhgrid,pos=(0,0))
		self.speedgrid.Add(self.rpmgrid,pos=(1,0))
		grid.Add(self.speedgrid, pos=(1,2))
		self.SetBackgroundColour((0,0,0))
		
		###gangschaltung
		self.graf_handles['gang'] = {}
		self.graf_handles['gang']['n'] = wx.Image()
		self.graf_handles['gang']['n'].LoadFile('zahl/n.jpg')
		self.graf_handles['gang']['r'] = wx.Image()
		self.graf_handles['gang']['r'].LoadFile('zahl/r.jpg')
		self.graf_handles['gang']['gang'] = 0 
		self.graf_handles['gang']['static'] = wx.StaticBitmap(self,wx.ID_ANY,self.graf_handles['gang']['n'].ConvertToBitmap())
		grid.Add(self.graf_handles['gang']['static'] , pos=(1,3))
		#####GRAFIK LOAD ########
		'''
		############weg machen###########
		self.handle = wx.Image()
		self.handle.LoadFile('zahl/0.jpg')
		#self.handle = self.handle.Resize((50,100),(0,0))
		self.handle = self.handle.Scale(50,100)
		self.handle1 = wx.Image()
		self.handle1.LoadFile('zahl/1.jpg')
		#self.handle1 = self.handle1.Resize((50,100),(0,0))
		self.handle1 = self.handle1.Scale(50,100)
		
		self.ht1 = wx.StaticBitmap(self,wx.ID_ANY,self.handle.ConvertToBitmap())
		grid.Add(self.ht1, pos=(1,1))
		##########wegmachen ###############
		'''
		
		self.tester = wx.StaticText(self, label='System Speed')
		self.tester.SetForegroundColour((255,255,255))
		grid.Add(self.tester, pos=(1,0))
		
		self.start_stop_bt = wx.Button(self,wx.ID_ANY, "Start") ##Start Stop Button
		grid.Add(self.start_stop_bt, pos=(0,1))
		#########################
		'''
		self.array_steer = {}
		row = 0
		grid3 = wx.GridBagSizer(hgap=100, vgap=1)
		
		while row <=100:
			self.array_steer[row] = wx.StaticText(self, label="",size=(50,1))
			grid3.Add(self.array_steer[row],pos=(row,1))
			tt = row * 2
			gg = wx.Colour(1,tt,1)
			#grid3.SetDefaultCellBackgroundColour(gg)
			
			self.array_steer[row].SetOwnBackgroundColour(gg)
			#self.array_steer[row].SetBackgroundColour(gg)
			row += 1
		grid.Add(grid3, pos=(1,3))
		'''
		#################
		row = 2
		column = 0
		num = 1
		self.array_dash = {}
		while column < 6:
			while row <=12:
				self.array_dash[num] = wx.StaticText(self, label="number "+str(num),size=(100,20))
				self.array_dash[num].SetForegroundColour((255,255,255))
				grid.Add(self.array_dash[num], pos=(row,column))
				row += 1
				num += 1
			
			row = 2
			column +=1 

		self.CreateStatusBar() # A StatusBar in the bottom of the window

		filemenu= wx.Menu()
		
		# wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
		menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

		hSizer.Add(grid, 0, wx.ALL, 5)

		mainSizer.Add(hSizer, 0, wx.ALL, 5)
		
		####BIND AREA########
		self.grd = grid
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_BUTTON, self.on_off, self.start_stop_bt)
		
		self.inter = 0
		self.SetSizerAndFit(mainSizer)
		#timer set#
		self.abfragetimer = wx.Timer()
		self.abfragetimer.Bind(wx.EVT_TIMER, self.dispatcher_call)

		################FPS ANZEIGER ######
		dt = datetime.now()
		self.wc = 0
		self.Sec_now = dt.second
		self.sec = {}
		self.loopc = 0
			
		self.Show(True)
	
	def on_off (self,e):
		
		'''
		#alte PDAL anzeige 
		t = 1
		
		self.ht1.SetBitmap(self.handle1.ConvertToBitmap())
		print (dir (self.ht1)) 
		while t <= 100:
			gg = wx.Colour(0,0,0)
			#print (t)
			self.array_steer[t].SetOwnBackgroundColour(gg)
			t +=1
		'''
		if self.inter == 0:
			self.out_dispatcher.put(1)#einschalten
			self.abfragetimer.Start(20)
			self.start_stop_bt.SetLabel('Stop')
			self.inter = 1
		else:

			dt = datetime.now()
			self.Sec_now = dt.second
			self.inter = 0
			self.start_stop_bt.SetLabel('Start')
			self.out_dispatcher.put(0)
			self.abfragetimer.Stop()
	def dispatcher_call (self,e):

		########################
		dt = datetime.now()
		if int(self.Sec_now) != dt.second:
			calc = 0
			self.loopc +=1
			if self.sec != {}:
				for x in self.sec:
					if x != 0:
						new = x - 1
						calc += self.sec[x] - self.sec[new]
				mstime = round(round(calc / self.wc)/1000000,2)
				data = "FPS: {}, React: {}".format(self.wc,mstime)
				self.tester.SetLabel(data)
				
			
			self.sec = {}
			self.Sec_now = dt.second
			self.wc = 0
		
		self.sec[self.wc] = dt.microsecond
		self.wc += 1
		#######################

		self.quote.SetLabel('dispatcher_call')
		h = {}
		while self.in_dispatcher.empty() != True:
			###
			h = self.in_dispatcher.get()
		
		if h != {}:
			for x in h:
				str_no = str(x)
				if math.isnan(h[x]) != True:
					self.array_dash[x].SetLabel(str(round(h[x])))
				else:
					self.array_dash[x].SetLabel('muller')
					
					#self.array_dash['2_0'].SetLabel(round(h[1],2))
			##### RPM ANZEIGE
			a = str(round(h[38]*10))
			while len(a) <= 3:
				a = '0'+a
				#print(a)
			c = 0
			while c <= 3:
				#print (a)
				self.graf_handles['gfx_static'][str(c)+'r'].SetBitmap(self.graf_handles[a[c]+'g'].ConvertToBitmap())
				c += 1
			
			
			############### Gang auswahl ############# 
			
			
			if round(h[34]) != self.graf_handles['gang']['gang']:
				self.graf_handles['gang']['gang'] = round(h[34])
				s1 = str(self.graf_handles['gang']['gang'])
				if self.graf_handles['gang']['gang'] == 0:
					self.graf_handles['gang']['static'].SetBitmap(self.graf_handles['gang']['n'].ConvertToBitmap())
				elif self.graf_handles['gang']['gang'] == 10:
					print ('lalal')
				else:
					self.graf_handles['gang']['static'].SetBitmap(self.graf_handles[s1+'o'].ConvertToBitmap())
			
			
			#self.graf_handles['gang']['static']
			#self.graf_handles['gang']['r']
			#self.graf_handles['gang']['n']
				

	def OnAbout(self,e):
		self.mes = wx.Gauge(self,id=66, range=10, pos=(200,200),name='ttx')
		# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
		dlg = wx.MessageDialog( self, "Vroom Vroom", "Vroom Vroom Ultra", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.

	def OnExit(self,e):
		self.out_dispatcher.put('off')#runter fahre
		self.Close(True)  # Close the frame.

if __name__ == '__main__':
	
	stacker = {}
	stacker['disp1'] = Queue() #Windows to Dispatcher
	stacker['disp2'] = Queue() #Dispatcher to Windows
	stacker['udp1'] = Queue()#Dispatcher to UDP
	stacker['udp2'] = Queue()#UDP to Dispatcher
	stacker['disp_proc'] = Process(target=dispatcher,args=(stacker['disp1'], stacker['disp2'],stacker['udp1'], stacker['udp2']))
	stacker['disp_proc'].start()
	stacker['udp_proc'] = Process(target=udp_control,args=(stacker['udp1'], stacker['udp2'],  stacker['disp2']))
	stacker['udp_proc'].start()

	
	a = str(24)
	print (len(a))
	
	app = wx.App(False)
	frame = MainWindow(None, "Vroom  Vroom",stacker['disp1'], stacker['disp2'] )
	app.MainLoop()
	
	if stacker['disp_proc'].is_alive() == True:
		stacker['disp_proc'].terminate()
	
	if stacker['udp_proc'].is_alive() == True:
		stacker['udp_proc'].terminate()
	
	'''
	dt = datetime.now()
	print (dir (dt))
	wc = 0
	Sec_now = dt.second
	sec = {}
	loopc = 0
	while True:
		dt = datetime.now()
		#print (dt.second)
		if Sec_now != dt.second:
			calc = 0
			loopc +=1 
			for x in sec:
				if x != 0:
					new = x - 1
					calc += sec[x] - sec[new]
			
			mstime = round(round(calc / wc)/1000000,2)
			data = "FPS: {}, React: {}".format(wc,mstime)
			print (data)
			
			sec = {}
			Sec_now = dt.second
			wc = 0
		
		sec[wc] = dt.microsecond
			
		#print (sec)
		
		wc += 1
		
		time.sleep(0.02)
		
		if loopc >= 10:
			break
	
	#time.sleep(1)
	'''
	
	'''
	lopper = 0
	on = 1
	stacker['disp1'].put(1)#einschalten
	time.sleep(1)
	while True:
		lopper += 1
		time.sleep(0.5)
		#print ('main:LOOP')
		if stacker['disp2'].empty() != True:
			#print('##################')
			if on == 1:
				#Print('MASTER PRITN')
				h = stacker['disp2'].get()
				
				print (round(h[1],2))
			else:
				
				if stacker['disp2'].get() == 'ok':
					#print ('master halt')
					break
		
		if lopper == 20:
			#print ('CLOSE MAIN')
			on = 0
			stacker['disp1'].put('off')#runter fahren

'''