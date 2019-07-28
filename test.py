from urllib.request import urlretrieve
import requests
import json
import urllib3
import shutil
import os

from tkinter import *
from tkinter import ttk
from tkinter.ttk import * 
from tkinter import Menu 
from PIL import ImageTk, Image


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

		print(json.dumps(location[1], indent = 5))
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


def createGUI(coords):
	x = 1965
	y = 897

	# resizeImgs()
	window = Tk()
	window.title("CCMN")
	window.geometry(str(x) + "x" + str(y))

	# ###### MENU #####
	style = ttk.Style()

	style.theme_create( "yummy", parent="alt", 
	settings=
	{
		"TNotebook": {"configure": {"tabmargins": [20, 10, 0, 20] } },
		"TNotebook.Tab": {
		"configure": {"padding": [50, 10], "background": 'white' },
		"map":       {"background": [("selected", 'cyan')],
		"expand": [("selected", [0, 0, 0, 0])] } } 
	} 
		)

	style.theme_use("yummy")

	tab_control = ttk.Notebook(window)
	tab1 = ttk.Frame(tab_control)  
	tab2 = ttk.Frame(tab_control)
	tab3 = ttk.Frame(tab_control)

	tab_control.add(tab1, text='1st Floor')  
	tab_control.add(tab2, text='2nd Floor')  
	tab_control.add(tab3, text='3rd Floor')  

	img1 = ImageTk.PhotoImage(Image.open("maps/1stFloor.jpg"))
	panel1 = Label(tab1, image = img1)
	panel1.grid(column = 20, row = 30)

	img2 = ImageTk.PhotoImage(Image.open("maps/2ndFloor.jpg"))
	panel2 = Label(tab2, image = img2)
	panel2.grid(column = 20, row = 30)

	img3 = ImageTk.PhotoImage(Image.open("maps/3rdFloor.jpg"))
	panel3 = Label(tab3, image = img3)
	panel3.grid(column = 20, row = 30)

	tab_control.pack(expand=1, fill='both')
	#######################################



	window.mainloop()

def main():
	########## CMX #########
	urlCMX = "https://cisco-cmx.unit.ua"
	usernameCMX = "RO"
	passwordCMX = "just4reading"

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
	coords = takeCooords(urlCMX, passwordCMX, usernameCMX)
	


	# try:
	# 	mapdata = requests.request("GET", endpoint, auth=(username, password), verify=False)
	# 	print("got maps")
	# 	# mapdatajson = json.loads(mapdata.text)
	# 	print(json.dumps(mapdata.json(), indent=4))

	# except Exception as e:
	# 	print(e)


	###### GUI ######
	createGUI(coords)

if __name__ == "__main__":
	main()