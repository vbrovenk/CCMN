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
av_dwell = "/api/presence/v1/dwell/average"
peak_hour = "/api/presence/v1/visitor/today/peakhour"
hourly = "/api/presence/v1/visitor/hourly"
########## 3DAYS AND 7DAYS #########
# connected = "/api/presence/v1/connected/total"
# visitors = "/api/presence/v1/visitor/total"
# repeat = "/api/presence/v1/repeatvisitors/total"
# passerby = "/api/presence/v1/passerby/total"

# percentage_of_connected_visitors = round(total_connected / total_visitors * 100)

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


# def takeConnectedDevices(id, url, password, username, mainWindow):
# 	devices = visitors + mainWindow.day + "?siteId=" + str(id)
# 	answer = takeRequest(url, devices, username, password)
# 	# print(devices)
# 	# print(answer)
# 	return (answer)

def takeConnectedDevices(id, url, password, username, mainWindow):
	devices = connected + mainWindow.day + "?siteId=" + str(id)
	answer = takeRequest(url, devices, username, password)
	# print(connected)
	# print(devices)
	# print("HERE")
	return (answer)

def takeAllVisitors(id, url, password, username, mainWindow):
	devices = visitors + mainWindow.day + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	# print(answer)
	return (answer)

def takeRepeatVisitors(id, url, password, username, mainWindow):
	devices = repeat + mainWindow.day + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	# print(answer)
	return (answer)

def takeDwellTime(id, url, password, username, mainWindow):
	devices = dwell + mainWindow.day + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	# print(answer)
	return (list(answer.values()))

def takeavDwellTime(id, url, password, username, mainWindow):
	devices = av_dwell + mainWindow.day + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	# print(answer)
	return (round(answer))

def takePeakHour(id, url, password, username):
	devices = peak_hour + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	# print(answer)
	return (answer)

def takePeakHourVisitors(id, url, password, usernamem, mainWindow):
	devices = hourly + mainWindow.day + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	# print(answer)
	return (answer)
