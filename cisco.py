import requests
import json


connected = "/api/presence/v1/connected/count"


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
