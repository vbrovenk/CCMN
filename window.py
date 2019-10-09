import graph
from dateutil.relativedelta import relativedelta
import json
from tkinter import *
from tkcalendar import *
from tkinter import ttk
from threading import Thread
import datetime
from PIL import ImageTk, Image
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkinter import messagebox

class Window:
	def __init__(self, request):
		self.x = 1965
		self.y = 897

		self.request = request

		self.request.getFloorImage()

		self.window = Tk()
		self.window.title("CCMN")
		self.window.geometry(str(self.x) + "x" + str(self.y))

		#### NOTEBOOK ####
		self.main_notebook = ttk.Notebook(self.window)

		self.map_tab = Frame(self.main_notebook)
		self.presence_tab = Frame(self.main_notebook)

		self.map_tab.pack()
		self.presence_tab.pack()

		self.main_notebook.add(self.map_tab, text = "Map")
		self.main_notebook.add(self.presence_tab, text = "Presence")

		self.main_notebook.pack(expand=1, fill = BOTH)

		self.map_notebook = ttk.Notebook(self.map_tab)

		self.first_floor = Frame(self.map_notebook)
		self.second_floor = Frame(self.map_notebook)
		self.third_floor = Frame(self.map_notebook)

		self.first_floor.pack()
		self.second_floor.pack()
		self.third_floor.pack()

		self.map_notebook.add(self.first_floor, text = "1st Floor")
		self.map_notebook.add(self.second_floor, text = "2nd Floor")
		self.map_notebook.add(self.third_floor, text = "3rd Floor")

		self.map_notebook.place(x = 0, y = 0)

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
		week_ago = (datetime.datetime.today() - relativedelta(days = 7)).strftime("%Y-%m-%d")
		self.month_year = today.split("-")

		calendar_button = Button(self.presence_tab, text = "Choose Date Range", command = self.create_calendar)
		calendar_button.place(x = 1600, y = 40)
		
		self.startdate_entry = Entry(self.presence_tab)
		self.startdate_entry.place(x = 1600, y = 65)
		self.startdate_entry.insert(0, week_ago)

		start_label = Label(self.presence_tab, text = "Start Date")
		start_label.place(x = 1525, y = 68)
		
		self.enddate_entry = Entry(self.presence_tab)
		self.enddate_entry.place(x = 1600, y = 95)
		self.enddate_entry.insert(0, today)

		end_label = Label(self.presence_tab, text = "End Date")
		end_label.place(x = 1525, y = 98)

		tmp = Button(self.presence_tab, text = "Change", command = self.change)
		tmp.place(x = 1600, y = 130)

		self.frame = Frame(self.presence_tab, background = "white", width=1000, height=110, borderwidth = 4)
		self.frame.place(x = 350, y = 100)

		self.visitors_label = Label(self.frame, text = "")
		self.dwelltime_label = Label(self.frame, text = "")
		self.peakhour_label = Label(self.frame, text = "")
		self.conversion_label = Label(self.frame, text = "")

		self.presence_note = ttk.Notebook(self.presence_tab)
		self.repeatVisitorsGraphTab = Frame(master=self.presence_note)
		self.dwellTimeGraphTab = Frame(master=self.presence_note)
		self.proximityGraphTab = Frame(master=self.presence_note)

		self.repeatVisitorsGraphTab.grid(row = 0, column = 0)
		self.dwellTimeGraphTab.grid(row = 0, column = 1)
		self.proximityGraphTab.grid(row = 0, column = 2)

		self.presence_note.add(self.repeatVisitorsGraphTab, text='Repeat Visitors')
		self.presence_note.add(self.dwellTimeGraphTab, text='Dwell Time')
		self.presence_note.add(self.proximityGraphTab, text='Proximity')

		self.repeatVisitorsGraph = graph.Graph(self.request, self.repeatVisitorsGraphTab, 'Repeat Visitors')
		self.dwellTimeGraph = graph.Graph(self.request, self.dwellTimeGraphTab, 'Dwell Time')
		self.proximityGraph = graph.Graph(self.request, self.proximityGraphTab, 'Proximity')
		self.presence_note.place(x = 100, y = 270)
		
		self.firstFloor_oval = self.canvas1.create_oval(0, 0, 0, 0)
		self.secondFloor_oval = self.canvas2.create_oval(0, 0, 0, 0)
		self.thirdFloor_oval = self.canvas3.create_oval(0, 0, 0, 0)
		#### THREADS ####
		self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}

		self.a1 = Label(self.map_tab, text ="", font = "Avenir, 18", fg = '#666699')
		self.a2 = Label(self.map_tab, text ="", font = "Avenir, 18", fg = '#666699')
		self.a3 = Label(self.map_tab, text ="", font = "Avenir, 18", fg = '#666699')
		self.a4 = Label(self.map_tab, text ="", font = "Avenir, 18", fg = '#666699')

	def colorize_found(self):
		self.canvas1.delete("green1")
		self.canvas2.delete("green2")
		self.canvas3.delete("green3")
		if (self.floor == "1st_Floor"):
			self.firstFloor_oval = self.canvas1.create_oval(self.coordX - 10, self.coordY - 10, self.coordX + 10, self.coordY + 10, fill = '#ff0000', tags = "green1")
		if (self.floor == "2nd_Floor"):
			self.secondFloor_oval = self.canvas2.create_oval(self.coordX - 10, self.coordY - 10, self.coordX + 10, self.coordY + 10, fill = '#ff0000', tags = "green2")
		if (self.floor == "3rd_Floor"):
			self.thirdFloor_oval = self.canvas3.create_oval(self.coordX - 10, self.coordY - 10, self.coordX + 10, self.coordY + 10, fill = '#ff0000', tags = "green3")

	def give_info(self):
		coords = self.request.takeCooords()
		for device in coords:
			if (self.message.get() == device["macAddress"] or self.message.get() == device["userName"]):
				self.MACaddress = device["macAddress"]
				if device["ipAddress"]:
					self.ip = device["ipAddress"][0]
				else:
					self.ip = 'IP is not provided'
				self.floor = device["mapInfo"]["mapHierarchyString"].split('>')[2]
				self.ssid = device["ssId"]
				self.manufacturer = device["manufacturer"]
				self.coordX = device["mapCoordinate"]["x"]
				self.coordY = device["mapCoordinate"]["y"]
				self.coordX *= 0.82
				self.coordY *= 0.92
				self.colorize_found()

				return True

		return False

	def click(self):
		self.a1["text"] = ""
		self.a2["text"] = ""
		self.a3["text"] = ""
		self.a4["text"] = ""
		if (len(self.message.get()) > 0):
			if self.give_info() == True:
				self.a1["text"] = self.ip
				self.a1.place(x = 1500, y = 216)

				self.a2["text"] = self.floor
				self.a2.place(x = 1500, y = 296)

				self.a3["text"] = self.manufacturer
				self.a3.place(x = 1500, y = 376)

			else:
				self.a1["text"] = "Not Found"
				self.a1.place(x = 1500, y = 216)

		else:
			self.a1["text"] = "Empty Field"
			self.a1.place(x = 1500, y = 216)

	def printDevices(self, canvas, needFloor):
		previous_info = []
		last_connected = Label(self.map_tab, text = "", font = "Avenir, 26", fg = '#666699')
		last_connected.place(x = 300, y = 790)
		while True:
			if(self.thread_Floors[needFloor] == False):
				break
			info = self.request.takeCooords()
			mac = [i["macAddress"] for i in info]
			time.sleep(1)
			canvas.delete("all_ovals")
			for device in info:
				if (needFloor in device["mapInfo"]["mapHierarchyString"]):
					mapCoordinateX = device["mapCoordinate"]["x"]
					mapCoordinateY = device["mapCoordinate"]["y"]
					mapCoordinateX *= 0.82
					mapCoordinateY *= 0.92
					canvas.create_oval(mapCoordinateX - 3, mapCoordinateY - 3, mapCoordinateX + 3, mapCoordinateY + 3, fill='blue', tags = "all_ovals")
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
					last_connected["text"] = ""
					last_connected["text"] = "Hi, @" + xlogin + " or mac:" + str(item) +  " now is on the " + floor
			previous_info = info

	def createFields(self):
		self.message = StringVar()
		self.search_label = Label(self.map_tab, text = "Input Mac Adress", font = "Avenir, 14", fg = '#666699')
		self.search_label.place(x = 1350, y = 172)
		self.search_entry = Entry(self.map_tab, textvariable = self.message)
		self.search_entry.place(x = 1470, y = 170)
		self.search_button = Button(self.map_tab, text = "search", command = self.click)
		self.search_button.place(x = 1670, y = 170)

		self.Ip = Label(self.map_tab, text = "IP Address:", font = "Avenir, 18", fg = '#666699')
		self.Ip.place(x = 1350, y = 216)
		self.Floor = Label(self.map_tab, text = "Floor: ", font = "Avenir, 18", fg = '#666699')
		self.Floor.place(x = 1350, y = 296)
		self.Manufacturer = Label(self.map_tab, text = "Manufacturer: ", font = "Avenir, 18", fg = '#666699')
		self.Manufacturer.place(x = 1350, y = 376)
	
	def totalVisitors(self):
		connected = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "connected")
		all_visitors = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "visitors")
		unique = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "unique")
		percentage = round(connected / all_visitors * 100)
		return [unique, all_visitors, connected, percentage]

	def dwellTime(self):
		dwell = self.request.takeDwellTime(self.startdate_entry.get(), self.enddate_entry.get(), "dwell")
		dwell_average = self.request.takeDwellTime(self.startdate_entry.get(), self.enddate_entry.get(), "dwell_average")
		return [list(dwell.values()), round(dwell_average)]

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
			info = max(info.items(), key=lambda k: k[1])
			peakhour = info[0]
			peakhour_visitors = info[1]
		return [peakhour, peakhour_visitors, peakday]

	def conversionRate(self):
		total = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "visitors")
		passerby = self.request.takeTotalVisitors(self.startdate_entry.get(), self.enddate_entry.get(), "passerby")
		conversion_rate = round(total * 100 / (total + passerby))
		return [conversion_rate, total, passerby]

	def total_visitors_label(self):
		total_visitors = self.totalVisitors()

		box = Listbox(self.frame,
						width=21,
						height=4,
						bg="#0D8105",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir, 18"),
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
				bg="#0D9004",
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
						bg="#CA0707",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir, 18"),
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
				bg="#EB0606",
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
						bg="#0885B4",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir, 18"),
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
				bg="#0792C6",
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
						bg="#DFAF2F",
						selectbackground="#5EAA5A",
						relief=RAISED,
						font=("Avenir, 18"),
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
				bg="#F0BC32",
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
		self.calendar = Calendar(top, bordercolor = "black", font = "Times 20", background = "white", 
										weekendforeground = "black", disableddayforeground = "#686564", showothermonthdays = False, 
										showweeknumbers = False, foreground = "black", selectforeground = "blue", selectbackground = "blue", 
										selectmode = "day", year = int(self.month_year[0]), month = int(self.month_year[1]), date_pattern = "y-mm-dd", maxdate = datetime.datetime.today())
		self.calendar.pack(fill = BOTH, expand = 1)
		from_button = Button(top, text = "Start Date", command = self.takeStartDate)
		from_button.pack(side = LEFT)
		to_button = Button(top, text = "End Date", command = self.takeEndDate)
		to_button.pack(side = RIGHT)

	def date_is_correct(self):
		start = self.startdate_entry.get()
		start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
		end = self.enddate_entry.get()
		end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
		if end_date < start_date:
			return False
		return True

	def change(self):
		if self.date_is_correct():
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
		else:
			messagebox.showinfo("Error", "End date can't be less than start date")

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
			thread2 = Thread(target=self.printDevices, args=(self.canvas2, "2nd_Floor",), daemon=True)
			thread2.start()
		if tab_text == "3rd Floor":
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":True}
			thread3 = Thread(target=self.printDevices, args=(self.canvas3, "3rd_Floor",), daemon=True)
			thread3.start()
		if (tab_text == "Presence"):
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}

	def on_tab_selected(self, event):
		selected_tab = event.widget.select()
		tab_text = event.widget.tab(selected_tab, "text")
		
		if (tab_text == "Map"):
			self.map_notebook.bind("<<NotebookTabChanged>>", lambda event, arg1 =self.canvas1, arg2 = self.canvas2, arg3 = self.canvas3: self.on_map_tab_selected(event, arg1, arg2, arg3))

		if (tab_text == "Presence"):
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}
			self.change()

	def start(self):
		self.main_notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
		self.window.mainloop()