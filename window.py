import requests
import json

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

from threading import Thread
import time

class Window:

	urlCMX = "https://cisco-cmx.unit.ua"
	usernameCMX = "RO"
	passwordCMX = "just4reading"

	def __init__(self):
		self.x = 1965
		self.y = 897

		self.window = Tk()
		self.window.title("CCMN")
		self.window.geometry(str(self.x) + "x" + str(self.y))

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

		self.tab1.pack()
		self.tab2.pack()
		self.tab3.pack()

		self.tab_control.add(self.tab1, text='1st Floor')
		self.tab_control.add(self.tab2, text='2nd Floor')
		self.tab_control.add(self.tab3, text='3rd Floor')

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

		self.message = StringVar()
		self.label = Label(self.window, text = "Input Mac Adress")
		self.label.place(x = 1300, y = 124)
		self.entry = Entry(self.window, textvariable = self.message)
		self.entry.place(x = 1420, y = 120)
		self.button = Button(self.window, text = "search", command = self.click)
		self.button.place(x = 1620, y = 120)

		#### MAC ADRESS ####
		self.ssid = StringVar()
		self.floor = StringVar()
		self.manufacturer = StringVar()
		self.coordX = DoubleVar()
		self.coordY = DoubleVar()
		
		#### THREADS ####
		self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}


	def give_info(self):
		coords = self.takeCooords(Window.urlCMX, Window.passwordCMX, Window.usernameCMX)
		print(json.dumps(coords, indent=5))
		for device in coords:
			if (self.message.get() in device["macAddress"]):
				self.floor = device["mapInfo"]["mapHierarchyString"].split('>')[2]
				self.ssid = device["ssId"]
				self.manufacturer = device["manufacturer"]
				self.coordX = device["mapCoordinate"]["x"]
				self.coordY = device["mapCoordinate"]["y"]
				# print ("%s, %s, %s, %f, %f" % (self.ssid, self.floor, self.manufacturer, self.coordX, self.coordY))
				return True

		return False
		

	def clear(self):
		self.entry.delete(0, END)

	def click(self):
		if (len(self.message.get()) > 0):
			if self.give_info() == True:
				answer = Label(self.window, text = self.floor)
				answer2 = Label(self.window, text = self.manufacturer)
				
				answer.place(x = 1300, y = 140)
				answer2.place(x = 1300, y = 160)
				
				print("True")
			else:
				frame = Label(self.window, text = "Not Found")
				frame.place(x = 1300, y = 140)
				print("False")
			self.clear()
		else:
			frame = Label(self.window, text = "Empty field")
			frame.place(x = 1300, y = 140)
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
					canvas.create_oval(mapCoordinateX - 3, mapCoordinateY - 3, mapCoordinateX + 3, mapCoordinateY + 3, fill='blue')

	def on_tab_selected(self, event, canvas1, canvas2, canvas3):
		selected_tab = event.widget.select()
		tab_text = event.widget.tab(selected_tab, "text")

		thread1 = Thread(target=self.printDevices, args=(self.canvas1, "1st_Floor",))
		thread2 = Thread(target=self.printDevices, args=(self.canvas2, "2nd_Floor",))
		
		if tab_text == "1st Floor":
			self.thread_Floors = {"1st_Floor":True, "2nd_Floor":False, "3rd_Floor":False}
			thread1.start()

		if tab_text == "2nd Floor":
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":True, "3rd_Floor":False}
			thread2.start()
			print("second floor")
		if tab_text == "3rd Floor":
			self.thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":True}
			thread3 = Thread(target=self.printDevices, args=(self.canvas3, "3rd_Floor",))
			thread3.start()
			print("third floor")

	def start(self):
		self.tab_control.bind("<<NotebookTabChanged>>", lambda event, arg1 =self.canvas1, arg2 = self.canvas2, arg3 = self.canvas3: self.on_tab_selected(event, arg1, arg2, arg3))
		self.window.mainloop()
