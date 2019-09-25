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

def getFloorImage(url, username, password, mapdatajson):
	mapImages = []
	try:
		os.mkdir("./maps")
		# TODO: remove /maps from git
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

########## INFO #########
url = "https://cisco-presence.unit.ua" # TODO: remove
username = "RO"
password = "Passw0rd"

urlCMX = "https://cisco-cmx.unit.ua"
usernameCMX = "RO"
passwordCMX = "just4reading"

########## API'S #########
sites = "/api/config/v1/sites"
connected = "/api/presence/v1/connected/count"
visitors = "/api/presence/v1/visitor/count"
repeat = "/api/presence/v1/repeatvisitors/count"

def takeSiteId(url, username, password): # TODO: move to cisco
	data = takeRequest(url, sites, username, password)
	id = data[0]["aesUId"]
	# print(id)
	return (id)


def takeRequest(url, restAPI, username, password): # TODO: move to cisco
	endpoint = url + restAPI
	# print("CHECK: " + endpoint)
	# print("Try URL: " + endpoint)
	data = None
	try:
		returnData = requests.request("GET", endpoint, auth=(username, password), verify=False)
		data = json.loads(returnData.text)
	except Exception as e:
		print(e)
	return (data)

def resizeImgs():
	width = 1280
	height = 720

	# TODO: no hardcode, connect with imgName
	im1 = Image.open("maps/domain_4_1511041548007.png")
	im5 = im1.resize((width, height), Image.ANTIALIAS)
	im5.save("maps/1stFloor" + ".jpg")

	im1 = Image.open("maps/domain_4_1513769867616.png")
	im5 = im1.resize((width, height), Image.ANTIALIAS)
	im5.save("maps/2ndFloor" + ".jpg")

	im1 = Image.open("maps/domain_4_1513775294059.png")
	im5 = im1.resize((width, height), Image.ANTIALIAS)
	im5.save("maps/3rdFloor" + ".jpg")

#Get Images of Maps
	# mapdatajson = takeRequest(urlCMX, "/api/config/v1/maps", usernameCMX, passwordCMX)
	# getFloorImage(urlCMX, usernameCMX, passwordCMX, mapdatajson)

def createGUI():


	# global id
	id = takeSiteId(url, username, password)
	###### CLASS ########
	mainWindow = Window(id)

	mainWindow.start()
	mainWindow.window.mainloop()

def main():
	###### GUI ######
	urllib3.disable_warnings()
	createGUI()

if __name__ == "__main__":
	main()