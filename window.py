import requests
import json

from tkinter import *
from tkcalendar import *
from tkinter import ttk
from PIL import ImageTk, Image

from threading import Thread
from datetime import date

import time

import cisco

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Window:

	urlCMX = "https://cisco-cmx.unit.ua"   # TODO useless
	usernameCMX = "RO"                     # TODO useless
	passwordCMX = "just4reading"           # TODO useless

	url = "https://cisco-presence.unit.ua" # TODO useless
	username = "RO"                        # TODO useless
	password = "Passw0rd"                  # TODO useless

	def graphic(self):
		# figure 20x1 inches
		fig = Figure(figsize=(20, 1))
		t = np.arange(0, 3, 0.01)
		fig.add_subplot().plot(t, 2 * np.sin(2 * np.pi * t))
		# place canvas in 4th bookmark
		canvas = FigureCanvasTkAgg(fig, master=self.tab4) # master ?
		# canvas.draw()
		canvas.get_tk_widget().pack(side=LEFT)
		cisco.takeRepeatVisitors(self.siteId, Window.url, Window.password, Window.username, "hourly")
		# OSAMOILE TODO: finish graphic
		# aka: number of repeat visitors over all available ranges
		# mb dwell time, Sum of Connected Visitor

		# TODO: Forecasting number of visitors (tomorrow)

		# TODO: session duration and the day of the week
		#       number of connections and the day of the week
		

	def __init__(self, siteId):
		self.x = 1965
		self.y = 897

		self.detector = False

		self.siteId = siteId # TODO useless

		self.window = Tk()
		self.window.title("CCMN")
		self.window.geometry(str(self.x) + "x" + str(self.y))

		self.day = "/today" # TODO useless
		# self.start_date = "2019-09-21"
		# self.end_date = "2019-09-21"

		self.style = ttk.Style()

		self.style.theme_create( "yummy", parent="alt", 
		settings=
		{
			"TNotebook": {"configure": {"tabmargins": [20, 10, 0, 20] } },
			"TNotebook.Tab": {
			"configure": {"padding": [50, 10], "background": 'white' },
			"map":       {"background": [("selected", 'cyan')],
			"expand": [("selected", [0, 0, 0, 0])] } } 
		})

		self.style.theme_use("yummy")

		#### NOTEBOOK ####
		self.style.theme_use("yummy")

		self.tab_control = ttk.Notebook(self.window)
		self.tab1 = Frame(self.tab_control)
		self.tab2 = Frame(self.tab_control)
		self.tab3 = Frame(self.tab_control)
		self.tab4 = Frame(self.tab_control)


		self.tab1.pack()
		self.tab2.pack()
		self.tab3.pack()
		self.tab4.pack()

		self.tab_control.add(self.tab1, text='1st Floor')
		self.tab_control.add(self.tab2, text='2nd Floor')
		self.tab_control.add(self.tab3, text='3rd Floor')
		self.tab_control.add(self.tab4, text='Presence')

		self.tab_control.pack(expand=1, fill='both')

		#### CANVAS ####
		# 1st
		self.canvas1 = Canvas(self.tab1, width=1280, height=720, bg='black')
		self.canvas1.pack(side='left')
		self.image1 = ImageTk.PhotoImage(Image.open("maps/1stFloor.jpg"))
		self.canvas1.create_image(0, 0, image = self.image1, anchor = 'nw')
		# 2nd
		self.canvas2 = Canvas(self.tab2, width=1280, height=720, bg='black')
		self.canvas2.pack(side='left')
		self.image2 = ImageTk.PhotoImage(Image.open("maps/2ndFloor.jpg"))
		self.canvas2.create_image(0, 0, image = self.image2, anchor = 'nw')
		# 3rd
		self.canvas3 = Canvas(self.tab3, width=1280, height=720, bg='black')
		self.canvas3.pack(side='left')

		self.image3 = ImageTk.PhotoImage(Image.open("maps/3rdFloor.jpg"))
		self.canvas3.create_image(0, 0, image = self.image3, anchor = 'nw')


		#### PRESENCE FRAME ####

		calendar_button = Button(self.tab4, text = "Choose Date Range", command = self.create_calendar)
		calendar_button.place(x = 1600, y = 40)

		self.startdate_entry = Entry(self.tab4)
		self.startdate_entry.place(x = 1600, y = 65)
		self.startdate_entry.insert(0, "2019-09-21")

		start_label = Label(self.tab4, text = "Start Date")
		start_label.place(x = 1525, y = 68)
		
		self.enddate_entry = Entry(self.tab4)
		self.enddate_entry.place(x = 1600, y = 95)
		self.enddate_entry.insert(0, "2019-09-21")

		end_label = Label(self.tab4, text = "End Date")
		end_label.place(x = 1525, y = 98)

		tmp = Button(self.tab4, text = "Change", command = self.change)
		tmp.place(x = 1600, y = 130)


		self.frame = Frame(self.tab4, highlightbackground = "green", highlightthickness=2, width=1000, height=110, borderwidth = 2)
		self.frame.place(x = 100, y = 100)

		self.visitors_label = Label(self.frame, text = "")
		self.dwelltime_label = Label(self.frame, text = "")
		self.peakhour_label = Label(self.frame, text = "")
		self.conversion_label = Label(self.frame, text = "")

		# self.frame.pack_propagate(False)
		#### MAC ADRESS ####
		self.MACaddress = StringVar()
		self.detectingControllers = StringVar()
		self.ssid = StringVar()
		self.floor = StringVar()
		self.manufacturer = StringVar()
		self.coordX = StringVar()
		self.coordY = StringVar()
		
		#### THREADS ####
		self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}

		self.a1 = Label(self.window, text ="")
		self.a2 = Label(self.window, text ="")
		self.a3 = Label(self.window, text ="")


	def give_info(self):
		coords = self.takeCooords(Window.urlCMX, Window.passwordCMX, Window.usernameCMX)
		print(json.dumps(coords, indent=5))
		for device in coords:
			if (self.message.get() == device["macAddress"]):
				self.MACaddress = device["macAddress"]
				# TODO: xlogin - get and display
				self.detectingControllers = device["detectingControllers"]
				self.floor = device["mapInfo"]["mapHierarchyString"].split('>')[2]
				self.ssid = device["ssId"]
				self.manufacturer = device["manufacturer"]
				self.coordX = str(device["mapCoordinate"]["x"])
				self.coordY = str(device["mapCoordinate"]["y"])
				# print ("%s, %s, %s, %f, %f" % (self.ssid, self.floor, self.manufacturer, self.coordX, self.coordY))
				return True

		return False
		

	def clear(self):
		self.entry.delete(0, END)

	def click(self):
		self.a1.destroy()
		self.a2.destroy()
		self.a3.destroy()
		if (len(self.message.get()) > 0):
			if self.give_info() == True:

				self.a1 = Label(self.window, text=self.MACaddress, font="Times 18", fg='#808080')
				self.a1.place(x = 1500, y = 220)
				self.a2 = Label(self.window, text=self.detectingControllers, font="Times 18", fg='#808080')
				self.a2.place(x = 1500, y = 300)
				self.a3 = Label(self.window, text="X: " + self.coordX + " Y: " + self.coordY, font="Times 18", fg='#808080')
				self.a3.place(x = 1500, y = 370)

				# answer = Label(self.window, text = self.floor)
				# answer2 = Label(self.window, text = self.manufacturer)
				
				# answer.place(x = 1300, y = 150)
				# answer2.place(x = 1300, y = 170)

				print("True")
			else:
				self.a1 = Label(self.window, text = "Not Found", font="Times 26", fg='#b30000')
				self.a1.place(x = 1300, y = 160)
				print("False")
				self.clear()
		else:
			self.a1 = Label(self.window, text = "Empty field", font="Times 26", fg='#b30000')
			self.a1.place(x = 1300, y = 160)
			print("False")
			self.clear()

	def takeRequest(self, url, restAPI, username, password):
		endpoint = url + restAPI
		print("Try URL: " + endpoint)
		data = None
		try:
			returnData = requests.request("GET", endpoint, auth=(username, password), verify=False)
			data = json.loads(returnData.text)
		except Exception as e:
			print(e)
		return (data)

	def takeCooords(self, url, password, username):
		location = None
		try:
			location = self.takeRequest(url, "/api/location/v2/clients", username, password)
			print("got data")
			# print(json.dumps(location, indent = 5))

		except Exception as e:
			print(e)
		return (location)


	def printDevices(self, canvas, needFloor):
		while True:
			if(self.thread_Floors[needFloor] == False):
				print("END: " + needFloor)
				break
			coords = self.takeCooords(Window.urlCMX, Window.passwordCMX, Window.usernameCMX)
			time.sleep(1)
			for device in coords:
				if (needFloor in device["mapInfo"]["mapHierarchyString"]):
					mapCoordinateX = device["mapCoordinate"]["x"]
					mapCoordinateY = device["mapCoordinate"]["y"]
					mapCoordinateX *= 0.82
					mapCoordinateY *= 0.92
					canvas.create_oval(mapCoordinateX - 3, mapCoordinateY - 3, mapCoordinateX + 3, mapCoordinateY + 3, fill='blue')
		# TODO:  "Hi, @xlogin or mac: 00:00:2a:01:00:06 now is on the first floor."

	def createFields(self):
		self.message = StringVar()
		self.label = Label(self.window, text = "Input Mac Adress")
		self.label.place(x = 1300, y = 124)
		self.entry = Entry(self.window, textvariable = self.message)
		self.entry.place(x = 1420, y = 120)
		self.button = Button(self.window, text = "search", command = self.click)
		self.button.place(x = 1620, y = 120)

		self.Mac = Label(self.window, text="MAC Address:", font="Times 26", fg='#666699')
		self.Mac.place(x = 1500, y = 170)
		self.Ip = Label(self.window, text="IP Address:", font="Times 26", fg='#666699')
		self.Ip.place(x = 1500, y = 250)
		self.Coords = Label(self.window, text="Co-ordinates:", font="Times 26", fg='#666699')
		self.Coords.place(x = 1500, y = 330)
	
	def totalVisitors(self):
		connected = cisco.takeTotalVisitors(self.siteId, Window.url, Window.password, Window.username, self, "connected")
		all_visitors = cisco.takeTotalVisitors(self.siteId, Window.url, Window.password, Window.username, self, "visitors")
		unique = cisco.takeTotalVisitors(self.siteId, Window.url, Window.password, Window.username, self, "unique")
		percentage = round(connected / all_visitors * 100)
		return [unique, all_visitors, connected, percentage]
	
	def dwellTime(self):
		dwell = cisco.takeDwellTime(self.siteId, Window.url, Window.password, Window.username, self, "dwell")
		average_dwell = cisco.takeDwellTime(self.siteId, Window.url, Window.password, Window.username, self, "average_dwell")
		return [list(dwell.values()), round(average_dwell)]

	def peakHour(self):
		peakhour = None
		peakhour_visitors = None
		peakday = None
		if self.startdate_entry.get() != self.enddate_entry.get():
			insights = cisco.takeInsights(self.siteId, Window.url, Window.password, Window.username, self, "month_peakhour")
			peakhour = insights["monthStats"]["peakHour"]
			peakhour_visitors = insights["monthStats"]["peakHourCount"]
			peakday = insights["monthStats"]["peakCount"]
		else:
			info = cisco.takeInsights(self.siteId, Window.url, Window.password, Window.username, self, "day_peakhour")
			# print (info.items()[0])##how it works!?
			info = max(info.items(), key=lambda k: k[1])
			peakhour = info[0]
			peakhour_visitors = info[1]
		return [peakhour, peakhour_visitors, peakday]

	def conversionRate(self):
		total = cisco.takeTotalVisitors(self.siteId, Window.url, Window.password, Window.username, self, "visitors")
		passerby = cisco.takeTotalVisitors(self.siteId, Window.url, Window.password, Window.username, self, "passerby")
		conversion_rate = round(total * 100 / (total + passerby))
		# print([conversion_rate, total, passerby])
		return [conversion_rate, total, passerby]

	def total_visitors_label(self):
		total_visitors = self.totalVisitors()

		box = Listbox(self.frame,
						width=21,
						height=4,
						bg="blue",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir", 18),
						fg = "white")

		box_info = [	"Unique Visitors " + str(total_visitors[0]),
						"Total Visitors " + str(total_visitors[1]),
						"Total Connected " + str(total_visitors[2]),
						"Percentage " + str(total_visitors[3]) + "%"]

		for info in box_info:
			box.insert(END, info)

		def click(event):
			box.grid(row = 1, column = 0)

		def forget(event):
			box.grid_forget()

		self.visitors_label = Label(self.frame, text='Total Visitors ' + str(total_visitors[1]),
				relief=RAISED,
				bg="blue",
				font=("Times New Roman", 30),
				fg='white')

		self.visitors_label.bind('<Button-1>', click)
		self.visitors_label.bind('<Leave>', forget)
		self.visitors_label.grid(row = 0, column = 0, padx = (0, 10))

	def dwell_time_label(self):
		dwell = self.dwellTime()
		
		box = Listbox(self.frame,
						width=33,
						height=5,
						bg="blue",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir", 18),
						fg = "white")

		box_info = [	"5-30 mins " + str(dwell[0][0]) + " visitors",
						"30-60 mins " + str(dwell[0][1]) + " visitors",
						"1-5 hours " + str(dwell[0][2]) + " visitors",
						"5-8 hours " + str(dwell[0][3]) + " visitors",
						"8+ hours " + str(dwell[0][4]) + " visitors"]

		for info in box_info:
			box.insert(END, info)

		def click(event):
			box.grid(row = 1, column = 1)

		def forget(event):
			box.grid_forget()

		self.dwelltime_label = Label(self.frame, text='Average Dwell Time ' + str(dwell[1]) + " mins",
				relief=RAISED,
				bg="blue",
				font=("Times New Roman", 30),
				fg='white')

		self.dwelltime_label.bind('<Button-1>', click)
		self.dwelltime_label.bind('<Leave>', forget)
		self.dwelltime_label.grid(row = 0, column = 1, padx = (0, 10))

	def peak_hour_label(self):
		peakhour = self.peakHour()
		box = Listbox(self.frame,
						width=19,
						height=1,
						bg="blue",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir", 18),
						fg = "white")

		box.insert(1, "Visitors in peak hour " + str(peakhour[1]))
		if (peakhour[2] != None):
			box["height"] = 2
			box.insert(2, "Visitors in peak day " + str(peakhour[2]))

		def click(event):
			box.grid(row = 1, column = 3)

		def forget(event):
			box.grid_forget()

		text = "Peak Hour " + str(peakhour[0]) + "-" + str(int(peakhour[0]) + 1)

		self.peakhour_label = Label(self.frame, text = text,
				relief=RAISED,
				bg="blue",
				font=("Times New Roman", 30),
				fg='white')

		self.peakhour_label.bind('<Button-1>', click)
		self.peakhour_label.bind('<Leave>', forget)
		self.peakhour_label.grid(row = 0, column = 3, padx = (0, 10))

	def conversion_rate_label(self):
		conversion_rate = self.conversionRate()

		box = Listbox(self.frame,
						width=24,
						height=3,
						bg="blue",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir", 18),
						fg = "white")

		box_info = [	"Conversion Rate " + str(conversion_rate[0]) + "%",
						"Total Visitors " + str(conversion_rate[1]),
						"Total Passerby " + str(conversion_rate[2])]

		for info in box_info:
			box.insert(END, info)

		def click(event):
			box.grid(row = 1, column = 4)

		def forget(event):
			box.grid_forget()

		self.conversion_label = Label(self.frame, text='Conversion Rate ' + str(conversion_rate[0]) + "%",
				relief=RAISED,
				bg="blue",
				font=("Times New Roman", 30),
				fg='white')

		self.conversion_label.bind('<Button-1>', click)
		self.conversion_label.bind('<Leave>', forget)
		self.conversion_label.grid(row = 0, column = 4)

	def takeStartDate(self):
		# self.start_date = self.calendar.get_date()
		self.startdate_entry.delete(0, END)
		self.startdate_entry.insert(0, self.calendar.get_date())
		# tmp = self.calendar.get_date().split("/")
		# # print (tmp)
		# day = tmp[1]
		# month = tmp[0]
		# year = "20" + str(tmp[2])
		# if (len(day) == 1):
		# 	day = "0" + day
		# if (len(month) == 1):
		# 	month = "0" + month
		# # print (year, " | ", month, " | ", day)
		# self.start_date = year + "-" + month + "-" + day
		# print ("start = " + self.start_date)

	def takeEndDate(self):
		self.enddate_entry.delete(0, END)
		self.enddate_entry.insert(0, self.calendar.get_date())
		# self.end_date = self.calendar.get_date()
		# # print (tmp)
		# day = tmp[1]
		# month = tmp[0]
		# year = "20" + str(tmp[2])
		# if (len(day) == 1):
		# 	day = "0" + day
		# if (len(month) == 1):
		# 	month = "0" + month
		# # print (year, " | ", month, " | ", day)
		# self.end_date = year + "-" + month + "-" + day
		# print ("end = " + self.end_date)

	def create_calendar(self):
		top = Toplevel(self.window)
		self.calendar = Calendar(top, font = "Times 14", selectbackground = "blue",  selectmode = "day", year = 2019, month = 9, date_pattern = "y-mm-dd", maxdate = date.today())
		self.calendar.pack()
		from_button = Button(top, text = "Start Date", command = self.takeStartDate)
		from_button.pack(side = LEFT)
		to_button = Button(top, text = "End Date", command = self.takeEndDate)
		to_button.pack(side = RIGHT)
		# TODO SBASNAKA: invalid data (unclickable, alert box, etc.)

	def change(self):
		self.visitors_label.destroy()
		self.dwelltime_label.destroy()
		self.peakhour_label.destroy()
		self.conversion_label.destroy()

		self.total_visitors_label()
		self.dwell_time_label()
		self.peak_hour_label()
		self.conversion_rate_label()

	def on_tab_selected(self, event, canvas1, canvas2, canvas3):
		selected_tab = event.widget.select()
		tab_text = event.widget.tab(selected_tab, "text")
		
		if tab_text != "Presence" and self.detector == False:
			self.createFields()
			self.detector = True

		thread1 = Thread(target=self.printDevices, args=(self.canvas1, "1st_Floor",), daemon=True)

		if tab_text == "1st Floor":
			self.thread_Floors = {"1st_Floor":True, "2nd_Floor":False, "3rd_Floor":False}
			thread1.start()

		if tab_text == "2nd Floor":
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":True, "3rd_Floor":False}
			thread2 = Thread(target=self.printDevices, args=(self.canvas2, "2nd_Floor",), daemon=True)
			thread2.start()
		if tab_text == "3rd Floor":
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":True}
			thread3 = Thread(target=self.printDevices, args=(self.canvas3, "3rd_Floor",), daemon=True)
			thread3.start()
		if (tab_text == "Presence"):
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}
			self.detector = False

			self.label.destroy()
			self.button.destroy()
			self.entry.destroy()
			self.Mac.destroy()
			self.Ip.destroy()
			self.Coords.destroy()

			self.change()
			# TODO SBASNAKA: conversion rate = Floor congestion


			# check = Button(self.tab4, text = "check", command = cisco.testsumvisitors(self.siteId, Window.url, Window.password, Window.username, self))
			# check.place(x = 1500, y = 100)

			# self.comboExample = ttk.Combobox(self.tab4, 
			# 							values=[
			# 									"Today", 
			# 									"Yesterday",
			# 									"Last 3 Days",
			# 									"Last 7 Days",
			# 									"Last 30 Days",
			# 									"This Month",
			# 									"Last Month"])
			# # print(dict(self.comboExample)) 
			# self.comboExample.place(x = 20, y = 320)
			# self.comboExample.current(0)

			# # print(self.comboExample.current(), self.comboExample.get())
			# self.comboExample.bind("<<ComboboxSelected>>", self.callbackFunc)
			self.graphic()


	def start(self):
		self.tab_control.bind("<<NotebookTabChanged>>", lambda event, arg1 =self.canvas1, arg2 = self.canvas2, arg3 = self.canvas3: self.on_tab_selected(event, arg1, arg2, arg3))


		
		self.window.mainloop()