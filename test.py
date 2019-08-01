from urllib.request import urlretrieve
import requests
import json
import urllib3
import shutil
import os

# from tkinter import *
# from tkinter import ttk
from tkinter.ttk import * 
from tkinter import Menu 
from PIL import ImageTk, Image

# from threading import Thread
# import time

from window import Window

urlCMX = "https://cisco-cmx.unit.ua"
usernameCMX = "RO"
passwordCMX = "just4reading"

def getFloorImage(url, username, password, mapdatajson):
	mapImages = []
	try:
		os.mkdir("./maps")
	except OSError:
		print("Creation of the directory is failed")
	# print(mapdatajson)
	for campus in mapdatajson["campuses"]:
		for building in campus["buildingList"]:
			for floor in building["floorList"]:
				mapImages.append(
					{
						"hierarchy" : campus["name"] + ">" + \
						building["name"] + ">" + \
						floor["name"],
						"image" : floor["image"],
						"gpsMarkers" : floor["gpsMarkers"]
					}
				)

				endpoint = url + \
				"/api/config/v1/maps/imagesource/" + \
				floor["image"]["imageName"]

				print("trying " + endpoint)
				try:
					response = requests.request("GET", endpoint, \
					auth=(username, password), stream=True, verify=False)
					print("Got Map")

					with open("./maps/" + \
					floor["image"]["imageName"], 'wb') as f:
						response.raw.decode_content = True
						shutil.copyfileobj(response.raw, f)
				except Exception as e:
					print(e)

def takeSiteId(url, username, password):
	data = takeRequest(url, sites, username, password)
	id = data[0]["aesUId"]
	return (id)


def takeRequest(url, restAPI, username, password):
	endpoint = url + restAPI
	print("Try URL: " + endpoint)
	data = None
	try:
		returnData = requests.request("GET", endpoint, auth=(username, password), verify=False)
		data = json.loads(returnData.text)
	except Exception as e:
		print(e)
	return (data)



def takeConnectedDevices(url, password, username):
	devices = connected + "/today" + "?siteId=" + str(id)
	answer = takeRequest(url, devices, username, password)
	# print(devices)
	print(answer)
	# return (answer)

def takeAllVisitors(url, password, username):
	devices = visitors + "/today" + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	print(answer)

def takeRepeatVisitors(url, password, username):
	devices = repeat + "/today" + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	print(answer)

def takeCooords(url, password, username):
	location = None
	try:
		location = takeRequest(url, "/api/location/v2/clients", username, password)
		print("got data")
		# print(json.dumps(location, indent = 5))

	except Exception as e:
		print(e)
	return (location)

########## API'S #########
sites = "/api/config/v1/sites"
connected = "/api/presence/v1/connected/count"
visitors = "/api/presence/v1/visitor/count"
repeat = "/api/presence/v1/repeatvisitors/count"

def resizeImgs():
	width = 1280
	height = 720

	im1 = Image.open("maps/domain_4_1511041548007.png")
	im5 = im1.resize((width, height), Image.ANTIALIAS)
	im5.save("maps/1stFloor" + ".jpg")

	im1 = Image.open("maps/domain_4_1513769867616.png")
	im5 = im1.resize((width, height), Image.ANTIALIAS)
	im5.save("maps/2ndFloor" + ".jpg")

	im1 = Image.open("maps/domain_4_1513775294059.png")
	im5 = im1.resize((width, height), Image.ANTIALIAS)
	im5.save("maps/3rdFloor" + ".jpg")


# thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":False}

# def printDevices(canvas, needFloor):
# 	while True:
# 		if(thread_Floors[needFloor] == False):
# 			break
# 		coords = takeCooords(urlCMX, passwordCMX, usernameCMX)
# 		time.sleep(1)
# 		for device in coords:
# 			if (needFloor in device["mapInfo"]["mapHierarchyString"]):
# 				mapCoordinateX = device["mapCoordinate"]["x"]
# 				mapCoordinateY = device["mapCoordinate"]["y"]
# 				canvas.create_oval(mapCoordinateX - 3, mapCoordinateY - 3, mapCoordinateX + 3, mapCoordinateY + 3, fill='blue')


# def on_tab_selected(event, canvas1, canvas2, canvas3):
# 	selected_tab = event.widget.select()
# 	tab_text = event.widget.tab(selected_tab, "text")

# 	global thread_Floors
# 	thread1 = Thread(target=printDevices, args=(canvas1, "1st_Floor",))
	
# 	if tab_text == "1st Floor":
# 		thread_Floors = {"1st_Floor":True, "2nd_Floor":False, "3rd_Floor":False}

# 		# thread1 = Thread(target=printDevices, args=(canvas1, "1st_Floor",))
# 		thread1.start()

# 	if tab_text == "2nd Floor":
# 		thread_Floors = {"1st_Floor":False, "2nd_Floor":True, "3rd_Floor":False}
# 		thread2 = Thread(target=printDevices, args=(canvas2, "2nd_Floor",))
# 		thread2.start()
# 		print("second floor")
# 	# if tab_text == "3rd Floor":
# 	# 	thread_Floors = {"1st_Floor":False, "2nd_Floor":False, "3rd_Floor":True}
# 	# 	thread3 = Thread(target=printDevices, args=(canvas3, "3rd_Floor",))
# 	# 	thread3.start()

# 		print("third floor")

def createGUI():

	# tab_control.bind("<<NotebookTabChanged>>", lambda event, arg1 =canvas1, arg2 = canvas2, arg3 = canvas3: on_tab_selected(event, arg1, arg2, arg3))

	# window.mainloop()

	###### CLASS ########
	mainWindow = Window()

	mainWindow.start()

def main():
	########## CMX #########
	# urlCMX = "https://cisco-cmx.unit.ua"
	# usernameCMX = "RO"
	# passwordCMX = "just4reading"

	###### PRECENSE #######
	url = "https://cisco-presence.unit.ua"
	username = "RO"
	password = "Passw0rd"

	# global id
	# id = takeSiteId(url, username, password)

	# takeConnectedDevices(url, password, username)
	# takeAllVisitors(url, password, username)
	# takeRepeatVisitors(url, password, username)

	# endpoint = url + "/api/presence/v1/visitor/count/today?siteId=1513804707441"
	# print(endpoint)

	#Get Images of Maps
	# mapdatajson = takeRequest(urlCMX, "/api/config/v1/maps", usernameCMX, passwordCMX)
	# getFloorImage(urlCMX, usernameCMX, passwordCMX, mapdatajson)
	
	
	#Take coords
	# coords = takeCooords(urlCMX, passwordCMX, usernameCMX)
	


	# try:
	# 	mapdata = requests.request("GET", endpoint, auth=(username, password), verify=False)
	# 	print("got maps")
	# 	# mapdatajson = json.loads(mapdata.text)
	# 	print(json.dumps(mapdata.json(), indent=4))

	# except Exception as e:
	# 	print(e)


	###### GUI ######
	createGUI()

if __name__ == "__main__":
	main()