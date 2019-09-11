import requests
import json

url = "https://cisco-presence.unit.ua"
username = "RO"
password = "Passw0rd"

########## API'S #########
sites = "/api/config/v1/sites"
########## TODAY AND YESTERDAY #########
connected = "/api/presence/v1/connected/count"
visitors = "/api/presence/v1/visitor/count"
repeat = "/api/presence/v1/repeatvisitors/count"
passerby = "/api/presence/v1/passerby/count"
dwell = "/api/presence/v1/dwell/count"
########## 3DAYS AND 7DAYS #########
# connected = "/api/presence/v1/connected/total"
# visitors = "/api/presence/v1/visitor/total"
# repeat = "/api/presence/v1/repeatvisitors/total"
# passerby = "/api/presence/v1/passerby/total"


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
	devices = dwell + mainWindow.day + "?siteId=" + str(id)
	answer = takeRequest(url, devices, username, password)
	# print(devices)
	print(answer)
	# return (answer)
