import requests
import json

from tkinter import *
from tkcalendar import *
from tkinter import ttk

from threading import Thread
import datetime
from dateutil.relativedelta import *
from PIL import ImageTk, Image
import time
import cisco
import graph

class Window:
	def __init__(self):
		self.x = 1965
		self.y = 897

		self.request = cisco.Request()
		self.detector = False

		self.window = Tk()
		self.window.title("CCMN")
		self.window.geometry(str(self.x) + "x" + str(self.y))

		self.style = ttk.Style()

		st = ttk.Style()

		self.style.theme_create( "yummy", parent="alt", 
		settings=
		{
			"TNotebook": {"configure": {"tabmargins": [10, 10, 0, 20] } },
			"TNotebook.Tab": {
			"configure": {"padding": [50, 10], "background": 'white' },
			"map":       {"background": [("selected", 'cyan')],
			"expand": [("selected", [0, 0, 0, 0])] } } 
		})
		st.configure("my.Calendar",
			font = "Times 20")

		# self.style.theme_use("yummy")

		# #### NOTEBOOK ####
		self.tab_control = ttk.Notebook(self.window)

		self.map_tab = Frame(self.tab_control)
		self.tab4 = Frame(self.tab_control)

		self.map_tab.pack()
		self.tab4.pack()

		self.tab_control.add(self.map_tab, text = "Map")
		self.tab_control.add(self.tab4, text = "Presence")

		self.tab_control.pack(expand=1, fill = BOTH)


		self.map_note = ttk.Notebook(self.map_tab)

		self.first_floor = Frame(self.map_note)
		self.second_floor = Frame(self.map_note)
		self.third_floor = Frame(self.map_note)

		self.first_floor.pack()
		self.second_floor.pack()
		self.third_floor.pack()

		self.map_note.add(self.first_floor, text = "1st Floor")
		self.map_note.add(self.second_floor, text = "2nd Floor")
		self.map_note.add(self.third_floor, text = "3rd Floor")

		self.map_note.place(x = 0, y = 0)


		#### CANVAS ####
		# 1st
		self.canvas1 = Canvas(self.first_floor, width=1280, height=720, bg='black')
		self.canvas1.pack(side='left')
		self.image1 = ImageTk.PhotoImage(Image.open("maps/1stFloor.jpg"))
		self.canvas1.create_image(0, 0, image = self.image1, anchor = 'nw')
		# 2nd
		self.canvas2 = Canvas(self.second_floor, width=1280, height=720, bg='black')
		self.canvas2.pack(side='left')
		self.image2 = ImageTk.PhotoImage(Image.open("maps/2ndFloor.jpg"))
		self.canvas2.create_image(0, 0, image = self.image2, anchor = 'nw')
		# 3rd
		self.canvas3 = Canvas(self.third_floor, width=1280, height=720, bg='black')
		self.canvas3.pack(side='left')

		self.image3 = ImageTk.PhotoImage(Image.open("maps/3rdFloor.jpg"))
		self.canvas3.create_image(0, 0, image = self.image3, anchor = 'nw')


		#### PRESENCE FRAME ####

		today = datetime.datetime.today().strftime("%Y-%m-%d")

		calendar_button = Button(self.tab4, text = "Choose Date Range", command = self.create_calendar)
		calendar_button.place(x = 1600, y = 40)

		self.startdate_entry = Entry(self.tab4)
		self.startdate_entry.place(x = 1600, y = 65)
		self.startdate_entry.insert(0, today)

		start_label = Label(self.tab4, text = "Start Date")
		start_label.place(x = 1525, y = 68)
		
		self.enddate_entry = Entry(self.tab4)
		self.enddate_entry.place(x = 1600, y = 95)
		self.enddate_entry.insert(0, today)

		end_label = Label(self.tab4, text = "End Date")
		end_label.place(x = 1525, y = 98)

		tmp = Button(self.tab4, text = "Change", command = self.change)
		tmp.place(x = 1600, y = 130)


		self.frame = Frame(self.tab4, background = "grey", width=1000, height=110, borderwidth = 4)
		self.frame.place(x = 100, y = 100)

		self.visitors_label = Label(self.frame, text = "")
		self.dwelltime_label = Label(self.frame, text = "")
		self.peakhour_label = Label(self.frame, text = "")
		self.conversion_label = Label(self.frame, text = "")


		self.presence_note = ttk.Notebook(self.tab4)
		self.repeatVisitorsGraphTab = Frame(master=self.presence_note)
		self.dwellTimeGraphTab = Frame(master=self.presence_note)
		self.proximityGraphTab = Frame(master=self.presence_note)

		self.repeatVisitorsGraphTab.grid(row = 0, column = 0)
		self.dwellTimeGraphTab.grid(row = 0, column = 1)
		self.proximityGraphTab.grid(row = 0, column = 2)

		self.presence_note.add(self.repeatVisitorsGraphTab, text='Repeat Visitors')
		self.presence_note.add(self.dwellTimeGraphTab, text='Dwell Time')
		self.presence_note.add(self.proximityGraphTab, text='Proximity')

		self.repeatVisitorsGraph = graph.Graph(self.repeatVisitorsGraphTab, 'Repeat Visitors')
		self.dwellTimeGraph = graph.Graph(self.dwellTimeGraphTab, 'Dwell Time')
		self.proximityGraph = graph.Graph(self.proximityGraphTab, 'Proximity')
		self.presence_note.place(x = 100, y = 270)

		# self.presence_note.bind("<<NotebookTabChanged>>", self.graph.changeTab) 	# OSAMOILE TODO: bind to tabs switching

		#### MAC ADRESS ####
		# self.MACaddress = StringVar()
		# self.detectingControllers = StringVar()
		# self.ssid = StringVar()
		# self.floor = StringVar()
		# self.manufacturer = StringVar()
		# self.coordX = StringVar()
		# self.coordY = StringVar()
		
		#### THREADS ####
		self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}

		self.a1 = Label(self.map_tab, text ="", font="Times 18", fg='#808080')
		self.a2 = Label(self.map_tab, text ="", font="Times 18", fg='#808080')
		self.a3 = Label(self.map_tab, text ="", font="Times 18", fg='#808080')
		self.a4 = Label(self.map_tab, text ="", font="Times 18", fg='#808080')


	def give_info(self):
		coords = self.request.takeCooords()
		# print(json.dumps(coords, indent=5))
		for device in coords:
			if (self.message.get() == device["macAddress"] or self.message.get() == device["userName"]):
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
		self.a1["text"] = ""
		self.a2["text"] = ""
		self.a3["text"] = ""
		self.a4["text"] = ""
		if (len(self.message.get()) > 0):
			if self.give_info() == True:
				self.a1["text"] = self.MACaddress
				self.a1.place(x = 1500, y = 220)

				self.a2["text"] = self.detectingControllers
				self.a2.place(x = 1500, y = 300)

				self.a3["text"] = "X = " + self.coordX + " Y = " + self.coordY
				self.a3.place(x = 1500, y = 370)

				self.a4["text"] = self.floor
				self.a4.place(x = 1500, y = 440)

				self.clear()
				# print("True")
			else:
				self.a1["text"] = "Not Found"
				self.a1.place(x = 1300, y = 160)
				# print("False")
				self.clear()
		else:
			self.a1["text"] = "Empty Field"
			self.a1.place(x = 1300, y = 160)
			# print("False")
			self.clear()

	def printDevices(self, canvas, needFloor):
		previous_info = []
		while True:
			if(self.thread_Floors[needFloor] == False):
				print("END: " + needFloor)
				break

			info = self.request.takeCooords()
			mac = [i["macAddress"] for i in info]
			time.sleep(1)
			for device in info:
				if (needFloor in device["mapInfo"]["mapHierarchyString"]):
					mapCoordinateX = device["mapCoordinate"]["x"]
					mapCoordinateY = device["mapCoordinate"]["y"]
					mapCoordinateX *= 0.82
					mapCoordinateY *= 0.92
					canvas.create_oval(mapCoordinateX - 3, mapCoordinateY - 3, mapCoordinateX + 3, mapCoordinateY + 3, fill='blue')
			if len(previous_info) > 0:
				previous_info = [i["macAddress"] for i in previous_info]
				difference = [item for item in mac if item not in previous_info]
				for item in difference:
					index = mac.index(item)
					floor = info[index]["mapInfo"]["mapHierarchyString"].split('>')[2]
					xlogin = info[index]["userName"]
					if (xlogin == ""):
						xlogin = "unknown"
					print ("Hi, @" + xlogin + " or mac:" + str(item) +  " now is on the " + floor)
			previous_info = info

	def createFields(self):
		self.message = StringVar()
		self.label = Label(self.map_tab, text = "Input Mac Adress")
		self.label.place(x = 1350, y = 124)
		self.entry = Entry(self.map_tab, textvariable = self.message)
		self.entry.place(x = 1470, y = 120)
		self.button = Button(self.map_tab, text = "search", command = self.click)
		self.button.place(x = 1670, y = 120)

		# TODO: remove mac address
		self.Mac = Label(self.map_tab, text = "MAC Address:", font = "Times 26", fg = '#666699')
		self.Mac.place(x = 1500, y = 170)
		self.Ip = Label(self.map_tab, text = "IP Address:", font = "Times 26", fg = '#666699')
		self.Ip.place(x = 1500, y = 250)
		self.Coords = Label(self.map_tab, text = "Co-ordinates:", font = "Times 26", fg = '#666699')
		self.Coords.place(x = 1500, y = 330)
		self.Floor = Label(self.map_tab, text = "Floor: ", font = "Times 26", fg = '#666699')
		self.Floor.place(x = 1500, y = 410)
	
	def totalVisitors(self):
		connected = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "connected")
		all_visitors = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "visitors")
		unique = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "unique")
		percentage = round(connected / all_visitors * 100)
		return [unique, all_visitors, connected, percentage]

	def totalVisitorsGraph(self):
		# if (self.startdate_entry.get() == self.enddate_entry.get()):
		# 	info = self.request.takeTotalVisitorsGraph(self, "hourly")
		# else:
		# 	info = self.request.takeTotalVisitorsGraph(self, "daily")
		info = self.request.takeTotalVisitorsGraph(self.startdate_entry.get(), self.enddate_entry.get()) ## mb no need in this func
		return info
	
	def dwellTime(self):
		dwell = self.request.takeDwellTime(self.startdate_entry.get(), self.enddate_entry.get(), "dwell")
		average_dwell = self.request.takeDwellTime(self.startdate_entry.get(), self.enddate_entry.get(), "average_dwell")
		return [list(dwell.values()), round(average_dwell)]
	
	def dwellTimeGraph(self):
		# if (self.startdate_entry.get() == self.enddate_entry.get()):
		# 	dwell = self.request.takeDwellTimeGraph(self, "hourly")
		# else:
		# 	dwell = self.request.takeDwellTimeGraph(self, "daily")
		dwell = self.request.takeDwellTimeGraph(self.startdate_entry.get(), self.enddate_entry.get()) ## mb no need in this func
		return dwell

	def makeForecast(self):
		period = (datetime.datetime.today() - relativedelta(months = 2)).strftime("%Y-%m-%d")
		tommorow = (datetime.datetime.today() + datetime.timedelta(days = 1)).strftime("%A")
		# print(period)
		connected = self.request.takeData('connected', period, self.enddate_entry.get())
		print (connected)
		visitors = self.request.takeData('visitor', period, self.enddate_entry.get())
		# print (visitors)
		passerby = self.request.takeData('passerby', period, self.enddate_entry.get())
		con_list = []
		vis_list = []
		pass_list = []
		for i in connected:
			splited = str(i).split("-")
			# print (splited)
			date = datetime.date(int(splited[0]), int(splited[1]), int(splited[2]))
			if date.strftime("%A") == tommorow:
				con_list.append(connected[i])
				vis_list.append(visitors[i])
				pass_list.append(passerby[i])
				# print(connected[i])
		for i in con_list:
			con_result = sum(con_list) / len(con_list)
			vis_result = sum(vis_list) / len(vis_list)
			pass_result = sum(pass_list) / len(pass_list)
		# print (con_result , vis_result, pass_result)
		# print (passerby)
		# print(tommorow)



	def peakHour(self):
		peakhour = None
		peakhour_visitors = None
		peakday = None
		if self.startdate_entry.get() != self.enddate_entry.get():
			insights = self.request.takeInsights(self.startdate_entry.get(), self.enddate_entry.get(), "month_peakhour")
			peakhour = insights["monthStats"]["peakHour"]
			peakhour_visitors = insights["monthStats"]["peakHourCount"]
			peakday = insights["monthStats"]["peakCount"]
		else:
			info = self.request.takeInsights(self.startdate_entry.get(), self.enddate_entry.get(), "day_peakhour")
			# print (info.items()[0])##how it works!?
			info = max(info.items(), key=lambda k: k[1])
			peakhour = info[0]
			peakhour_visitors = info[1]
		return [peakhour, peakhour_visitors, peakday]

	def conversionRate(self):
		total = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "visitors")
		passerby = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "passerby")
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
						width=20,
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
		self.startdate_entry.delete(0, END)
		self.startdate_entry.insert(0, self.calendar.get_date())

	def takeEndDate(self):
		self.enddate_entry.delete(0, END)
		self.enddate_entry.insert(0, self.calendar.get_date())

	def create_calendar(self):
		top = Toplevel(self.window)
		self.calendar = Calendar(top, bordercolor = "black", font = "Times 20", background = "white", weekendforeground = "black", disableddayforeground = "#686564", showothermonthdays = False, showweeknumbers = False, foreground = "black", selectforeground = "blue", selectbackground = "blue", selectmode = "day", year = 2019, month = 9, date_pattern = "y-mm-dd", maxdate = datetime.datetime.today())
		self.calendar.pack(fill = BOTH, expand = 1)
		from_button = Button(top, text = "Start Date", command = self.takeStartDate)
		from_button.pack(side = LEFT)
		to_button = Button(top, text = "End Date", command = self.takeEndDate)
		to_button.pack(side = RIGHT)

	def change(self):
		self.visitors_label.destroy()
		self.dwelltime_label.destroy()
		self.peakhour_label.destroy()
		self.conversion_label.destroy()

		self.total_visitors_label()
		self.dwell_time_label()
		self.peak_hour_label()
		self.conversion_rate_label()

		self.repeatVisitorsGraph.show(self.startdate_entry.get(), self.enddate_entry.get())
		self.dwellTimeGraph.show(self.startdate_entry.get(), self.enddate_entry.get())
		self.proximityGraph.show(self.startdate_entry.get(), self.enddate_entry.get())

		self.makeForecast()

	# def on_note_selected(self, event):
	# 	selected_tab = event.widget.select()
	# 	tab_text = event.widget.tab(selected_tab, "text")
	# 	self.presence_note.tab(self.presence_note.select(), "text")
	# 	if (tab_text == "Repeat Visitors"):
	# 		self.graph = graph.Graph(self.repeatVisitorsGraphTab, tab_text)
	# 	elif (tab_text == "")
	# 	self.graph.show(self.startdate_entry.get(), self.enddate_entry.get())
	# 	print(self.request.takeDwellTimeGraph(self.startdate_entry.get(), self.enddate_entry.get()))

	def on_map_tab_selected(self, event, canvas1, canvas2, canvas3):
		selected_tab = event.widget.select()
		tab_text = event.widget.tab(selected_tab, "text")

		self.createFields()

		thread1 = Thread(target=self.printDevices, args=(self.canvas1, "1st_Floor",), daemon=True)

		if tab_text == "1st Floor":
			self.thread_Floors = {"1st_Floor":True, "2nd_Floor":False, "3rd_Floor":False}
			thread1.start()

		if tab_text == "2nd Floor":
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":True, "3rd_Floor":False}
			print ("2 start, others stop")
			thread2 = Thread(target=self.printDevices, args=(self.canvas2, "2nd_Floor",), daemon=True)
			thread2.start()
		if tab_text == "3rd Floor":
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":True}
			thread3 = Thread(target=self.printDevices, args=(self.canvas3, "3rd_Floor",), daemon=True)
			thread3.start()
		if (tab_text == "Presence"):
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}
			self.detector = False


	def on_tab_selected(self, event):
		selected_tab = event.widget.select()
		tab_text = event.widget.tab(selected_tab, "text")
		
		if (tab_text == "Map"):
			self.map_note.bind("<<NotebookTabChanged>>", lambda event, arg1 =self.canvas1, arg2 = self.canvas2, arg3 = self.canvas3: self.on_map_tab_selected(event, arg1, arg2, arg3))

		if (tab_text == "Presence"):
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}
			self.change()

	def start(self):
		self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_selected)
		self.window.mainloop()