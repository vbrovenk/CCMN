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

########## API'S #########
sites = "/api/config/v1/sites"
visitors = "/api/presence/v1/visitor/count"
repeat = "/api/presence/v1/repeatvisitors/count"

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



def takeConnectedDevices(id, url, password, username, mainWindow):
	devices = connected + mainWindow.day + "?siteId=" + str(id)
	answer = takeRequest(url, devices, username, password)
	# print(devices)
	print(answer)
	# return (answer)

def takeAllVisitors(url, password, username, mainWindow):
	devices = visitors + mainWindow.day + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	print(answer)

def takeRepeatVisitors(url, password, username, mainWindow):
	devices = repeat + mainWindow.day + "?siteId=" + str(id)
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

url = "https://cisco-presence.unit.ua"
username = "RO"
password = "Passw0rd"

def createGUI():


	# global id
	id = takeSiteId(url, username, password)
	###### CLASS ########
	mainWindow = Window(id)

	mainWindow.start()
	takeConnectedDevices(id, url, password, username, mainWindow)
	# takeConnectedDevices(id, url, password, username, mainWindow)

def main():
	###### GUI ######
	createGUI()

if __name__ == "__main__":
	main()