import requests
import json

from tkinter import *
from tkcalendar import *
from tkinter import ttk
from PIL import ImageTk, Image

from threading import Thread
import time

import cisco

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Window:

	urlCMX = "https://cisco-cmx.unit.ua"
	usernameCMX = "RO"
	passwordCMX = "just4reading"

	url = "https://cisco-presence.unit.ua"
	username = "RO"
	password = "Passw0rd"

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
		

	def __init__(self, siteId):
		self.x = 1965
		self.y = 897

		self.detector = False

		self.siteId = siteId

		self.window = Tk()
		self.window.title("CCMN")
		self.window.geometry(str(self.x) + "x" + str(self.y))

		self.day = "/today"
		self.start_date = ""
		self.end_date = ""

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

		# # Presence

		# self.message = StringVar()
		# self.label = Label(self.window, text = "Input Mac Adress")
		# self.label.place(x = 1300, y = 124)
		# self.entry = Entry(self.window, textvariable = self.message)
		# self.entry.place(x = 1420, y = 120)
		# self.button = Button(self.window, text = "search", command = self.click)
		# self.button.place(x = 1620, y = 120)

		self.names_presence = ["Total Visitors", "Average Dwell Time", "Peak Hour", "Conversion Rate", "Top Device Maker"]
		self.labels_presence = []
		self.labels_colors = ["#FF3333", "#FDB800", "#92FD00", "#0064FD", "#D700FE"]


		self.total_visitors = self.totalVisitors()
		self.dwell = cisco.takeDwellTime(self.siteId, Window.url, Window.password, Window.username, self)
		self.av_dwell = cisco.takeavDwellTime(self.siteId, Window.url, Window.password, Window.username, self)
		self.peak_hour = cisco.takePeakHour(self.siteId, Window.url, Window.password, Window.username)
		# print (self.peak_hour)
		self.hourly = cisco.takePeakHourVisitors(self.siteId, Window.url, Window.password, Window.username, self)
		self.hourly = self.hourly[str(self.peak_hour)]
		# print (self.hourly)
		self.cliclable_menu_list = [self.total_visitors[0], "", 0 , 0, 0]
		#### PRESENCE FRAME ####

		# self.info_presence = []

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
		connected = cisco.takeConnectedDevices(self.siteId, Window.url, Window.password, Window.username, self)
		all_visitors = cisco.takeAllVisitors(self.siteId, Window.url, Window.password, Window.username, self)
		unique = all_visitors
		percentage = round(connected / all_visitors * 100)
		return [unique, all_visitors, connected, percentage]


	def callbackFunc(self, event):
		if (self.comboExample.current() == 0):
			self.day = "/today"
		elif(self.comboExample.current() == 1):
			self.day = "/yesterday"
		elif(self.comboExample.current() == 2):
			self.day = "/3days"
		elif(self.comboExample.current() == 3):
			self.day = "/lastweek"
		elif(self.comboExample.current() == 4):
			self.day = "/lastmonth"
		# elif(self.comboExample.current() == 1):
		# 	self.day = "today"
		# elif(self.comboExample.current() == 1):
		# 	self.day = "today"


	# def clickable_labels(self, event):
	# 	if (event.widget["bg"] == "#FF3333"): #checking clicked label according to the background color
	# 		print ("peak hour")
	# 	elif (event.widget["text"] == "Average Dwell Time"):
	# 		print ("peak hour")
	# 	elif (event.widget["text"] == "Peak Hour"):
	# 		print ("peak hour")
	# 	elif (event.widget["text"] == "Conversion Rate"):
	# 		print ("peak hour")
	# 	elif (event.widget["text"] == "Top Device Maker"):
	# 		print ("peak hour")
	# 	#need to make labels move


	def total_visitors_label(self):
		box = Listbox(self.tab4,
						width=21,
						height=4,
						bg="blue",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir", 18),
						fg = "white")

		box_info = [	"Unique Visitors " + str(self.total_visitors[1]),
						"Total Visitors " + str(self.total_visitors[0]),
						"Total Connected " + str(self.total_visitors[2]),
						"Percentage " + str(self.total_visitors[3]) + "%"]

		for info in box_info:
			box.insert(END, info)

		def click(event):
			box.place(x = 100, y = 150)

		def forget(event):
			box.place_forget()

		label = Label(self.tab4, text='Total Visitors ' + str(self.total_visitors[0]),
				relief=RAISED,
				bg="blue",
				font=("Times New Roman", 30),
				fg='white')

		label.bind('<Button-1>', click)
		label.bind('<Leave>', forget)
		label.place(x = 100, y = 100)

	def dwell_time_label(self):
		box = Listbox(self.tab4,
						width=33,
						height=5,
						bg="blue",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir", 18),
						fg = "white")

		box_info = [	"5-30 mins " + str(self.dwell[0]) + " visitors",
						"30-60 mins " + str(self.dwell[1]) + " visitors",
						"1-5 hours " + str(self.dwell[2]) + " visitors",
						"5-8 hours " + str(self.dwell[3]) + " visitors",
						"8+ hours " + str(self.dwell[4]) + " visitors"]

		for info in box_info:
			box.insert(END, info)

		def click(event):
			box.place(x = 400, y = 150)

		def forget(event):
			box.place_forget()

		label = Label(self.tab4, text='Average Dwell Time ' + str(self.av_dwell) + " mins",
				relief=RAISED,
				bg="blue",
				font=("Times New Roman", 30),
				fg='white')

		label.bind('<Button-1>', click)
		label.bind('<Leave>', forget)
		label.place(x = 400, y = 100)

	def peak_hour_label(self):
		box = Listbox(self.tab4,
						width=19,
						height=1,
						bg="blue",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir", 18),
						fg = "white")

		# box_info = [	"5-30 mins " + str(self.dwell[0]) + " visitors",
		# 				"30-60 mins " + str(self.dwell[1]) + " visitors",
		# 				"1-5 hours " + str(self.dwell[2]) + " visitors",
		# 				"5-8 hours " + str(self.dwell[3]) + " visitors",
		# 				"8+ hours " + str(self.dwell[4]) + " visitors"]

		# for info in box_info:
		# 	box.insert(END, info)
		box.insert(1, "Visitors in peak hour " + str(self.hourly))

		def click(event):
			box.place(x = 830, y = 150)

		def forget(event):
			box.place_forget()

		label = Label(self.tab4, text='Peak Hour ' + str(self.peak_hour) + "-" + str(self.peak_hour + 1),
				relief=RAISED,
				bg="blue",
				font=("Times New Roman", 30),
				fg='white')

		label.bind('<Button-1>', click)
		label.bind('<Leave>', forget)
		label.place(x = 830, y = 100)

	def takeStartDate(self):
		# self.start_date = self.calendar.get_date()
		tmp = self.calendar.get_date().split("/")
		# print (tmp)
		day = tmp[1]
		month = tmp[0]
		year = "20" + str(tmp[2])
		if (len(day) == 1):
			day = "0" + day
		if (len(month) == 1):
			month = "0" + month
		# print (year, " | ", month, " | ", day)
		self.start_date = year + "-" + month + "-" + day
		print ("start = " + self.start_date)

	def takeEndDate(self):
		tmp = self.calendar.get_date().split("/")
		# print (tmp)
		day = tmp[1]
		month = tmp[0]
		year = "20" + str(tmp[2])
		if (len(day) == 1):
			day = "0" + day
		if (len(month) == 1):
			month = "0" + month
		# print (year, " | ", month, " | ", day)
		self.end_date = year + "-" + month + "-" + day
		print ("end = " + self.end_date)

	def create_calendar(self):
		top = Toplevel(self.window)
		self.calendar = Calendar(top, font = "Times 14", selectmode = "day", year = 2019, month = 9)
		self.calendar.pack()
		from_button = Button(top, text = "Start Date", command = self.takeStartDate)
		from_button.pack(side = LEFT)
		to_button = Button(top, text = "End Date", command = self.takeEndDate)
		to_button.pack(side = RIGHT)


	def cleaner(self):
		for i in range(5):
			self.labels_presence[i].destroy()
		self.labelTop.destroy()
		self.comboExample.destroy()

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

			self.total_visitors_label()
			self.dwell_time_label()
			self.peak_hour_label()

			# for i in range(5):
			# 	self.labels_presence.append(
			# 		Label(self.tab4, text = self.names_presence[i] + " " + str(self.cliclable_menu_list[i]), font = ('Times', 24, 'bold'), bd=0, bg = self.labels_colors[i], fg = '#ffffff',
			# 		width = 22, height = 1))
			# 	self.labels_presence[i].place(x = 100 + i * 300, y = 100)
			# 	self.labels_presence[i].bind("<Button-1>", self.clickable_labels)
			# 	self.labels_presence[i].bind('<Leave>', self.clickable_menu.)

			self.labelTop = Label(self.tab4, text = "Choose your favourite month")
			self.labelTop.place(x = 20, y = 300)

			calendar_button = Button(self.tab4, text = "Calendar", command = self.create_calendar)
			calendar_button.place(x = 1600, y = 40)

			self.comboExample = ttk.Combobox(self.tab4, 
										values=[
												"Today", 
												"Yesterday",
												"Last 3 Days",
												"Last 7 Days",
												"Last 30 Days",
												"This Month",
												"Last Month"])
			# print(dict(self.comboExample)) 
			self.comboExample.place(x = 20, y = 320)
			self.comboExample.current(0)

			# print(self.comboExample.current(), self.comboExample.get())
			self.comboExample.bind("<<ComboboxSelected>>", self.callbackFunc)
			self.graphic()


	def start(self):
		self.tab_control.bind("<<NotebookTabChanged>>", lambda event, arg1 =self.canvas1, arg2 = self.canvas2, arg3 = self.canvas3: self.on_tab_selected(event, arg1, arg2, arg3))


		
		self.window.mainloop()