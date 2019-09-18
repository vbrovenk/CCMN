import requests
import json

url = "https://cisco-presence.unit.ua"
username = "RO"
password = "Passw0rd"

# https://cisco-presence.unit.ua/api/presence/v1/connected/total?siteId=1513804707441&startDate=2019-09-23&endDate=2019-09-27

########## API'S #########
sites = "/api/config/v1/sites"
########## TODAY AND YESTERDAY #########
test = "/api/presence/v1/connected/total"
connected = "/api/presence/v1/connected/count"
visitors = "/api/presence/v1/visitor/count"
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
day = "/today"

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

def takeEverything():
	# TODO: all requests
	# 0 self:)
	return 0

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

def takeRepeatVisitors(id, url, password, username, mode):
	devices = "/api/presence/v1/repeatvisitors/" + mode + day + "?siteId=" + str(id)
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	print(answer)
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

# "&startDate=" + mainWindow.start_date + "&endDate=" + mainWindow.end_date

def testsumvisitors(id, url, password, usernamem, mainWindow):
	devices = test + "?siteId=" + str(id) + "&startDate=" + mainWindow.start_date + "&endDate=" + mainWindow.end_date
	# print(devices)
	answer = takeRequest(url, devices, username, password)
	print(answer)
	# return (answer)
