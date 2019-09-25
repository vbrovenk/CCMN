import requests
import json

urlCMX = "https://cisco-cmx.unit.ua"
usernameCMX = "RO"
passwordCMX = "just4reading"

url = "https://cisco-presence.unit.ua"
username = "RO"
password = "Passw0rd"

# https://cisco-presence.unit.ua/api/presence/v1/connected/total?siteId=1513804707441&startDate=2019-09-23&endDate=2019-09-27

########## API'S #########
sites = "/api/config/v1/sites"
########## TODAY AND YESTERDAY #########
connected = "/api/presence/v1/connected/count"
peak_hour = "/api/presence/v1/visitor/today/peakhour"
########## 3DAYS AND 7DAYS #########
# connected = "/api/presence/v1/connected/total"
# visitors = "/api/presence/v1/visitor/total"
# repeat = "/api/presence/v1/repeatvisitors/total"
# passerby = "/api/presence/v1/passerby/total"
day = "/today"

# percentage_of_connected_visitors = round(total_connected / total_visitors * 100)

def takeRequest(url, restAPI, username, password):
	endpoint = url + restAPI
	# print("Try URL: " + endpoint)
	data = None
	try:
		returnData = requests.request("GET", endpoint, auth=(username, password), verify=False)
		# print(json.dumps(returnData, indent = 5))
		data = json.loads(returnData.text)
	except Exception as e:
		print(e)
	return (data)

########## ALL INFO ABOUT VISITORS #########

connected = "/api/presence/v1/connected/total"
visitors = "/api/presence/v1/visitor/total"
passerby = "/api/presence/v1/passerby/total"
unique = "/api/presence/v1/visitor/count"

def takeTotalVisitors(id, mainWindow, mode):
	if (mode == "connected"):
		devices = connected + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	elif (mode == "visitors"):
		devices = visitors + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	elif (mode == "passerby"):
		devices = passerby + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	else:
		devices = unique + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	answer = takeRequest(url, devices, username, password)
	# print (answer)
	return answer

daily_connected_graph = "/api/presence/v1/connected/daily"
daily_visitors_graph = "/api/presence/v1/visitor/daily"
daily_passerby_graph = "/api/presence/v1/passerby/daily"

hourly_connected_graph = "/api/presence/v1/connected/hourly"
hourly_visitors_graph = "/api/presence/v1/visitor/hourly"
hourly_passerby_graph = "/api/presence/v1/passerby/hourly"

def takeTotalVisitorsGraph(id, mainWindow, mode):
	answer = []
	if (mode == "daily"):
		connected = daily_connected_graph + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
		visitors = daily_visitors_graph + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
		passerby = daily_passerby_graph + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	elif (mode == "hourly"):
		connected = hourly_connected_graph + "?siteId=" + str(id) + "&date=" + mainWindow.startdate_entry.get()
		visitors = hourly_visitors_graph + "?siteId=" + str(id) + "&date=" + mainWindow.startdate_entry.get()
		passerby = hourly_passerby_graph + "?siteId=" + str(id) + "&date=" + mainWindow.startdate_entry.get()
	answer.append(takeRequest(url, connected, username, password))
	answer.append(takeRequest(url, visitors, username, password))
	answer.append(takeRequest(url, passerby, username, password))
	# print (answer)
	return answer

########## OVER ANY DATE RANGE #########


########## ALL INFO ABOUT DWELL TIME #########

dwell = "/api/presence/v1/dwell/count"
average_dwell = "/api/presence/v1/dwell/average"

def takeDwellTime(id, mainWindow, mode):
	if (mode == "dwell"):
		devices = dwell + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	elif (mode == "average_dwell"):
		devices = average_dwell + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	answer = takeRequest(url, devices, username, password)
	# print (answer)
	return answer


daily_dwelltime_graph = "/api/presence/v1/dwell/daily"
hourly_dwelltime_graph = "/api/presence/v1/dwell/hourly"

def takeDwellTimeGraph(id, mainWindow, mode):
	if (mode == "daily"):
		devices = daily_dwelltime_graph + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	elif (mode == "hourly"):
		devices = hourly_dwelltime_graph + "?siteId=" + str(id) + "&date=" + mainWindow.startdate_entry.get()
	answer = takeRequest(url, devices, username, password)
	# print (answer)
	return answer
########## OVER ANY DATE RANGE #########

##monthstats peakDay

########## ALL INFO ABOUT PEAK TIME #########

insights = "/api/presence/v1/insights"
hourly = "/api/presence/v1/visitor/hourly"

def takeInsights(id, mainWindow, mode):
	if (mode == "month_peakhour"):
		devices = insights + "?siteId=" + str(id) + "&startDate=" +  mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get()
	elif (mainWindow.startdate_entry.get() == mainWindow.enddate_entry.get() and mode == "day_peakhour"):
		devices = hourly + "/" + "?siteId=" + str(id) + "&date=" +  mainWindow.startdate_entry.get()
	# else:
	# 	devices = hourly + "?siteId=" + str(id) + "&date=" + mainWindow.start_date + "&endDate=" + mainWindow.end_date
	answer = takeRequest(url, devices, username, password)
	return answer

########## OVER ANY DATE RANGE #########


def takeCooords():
		location = None
		try:
			location = takeRequest(urlCMX, "/api/location/v2/clients", usernameCMX, passwordCMX)
			# print("got data")
			# print(json.dumps(location, indent = 5))

		except Exception as e:
			print(e)
		return (location)

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
	# print(answer)
	return (answer)

daily_repeat = "/api/presence/v1/repeatvisitors/daily"
hourly_repeat = "/api/presence/v1/repeatvisitors/hourly"

def repeat(id, mainWindow, mode):
	if (mode == "daily"):
		devices = daily_repeat + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get() ##if period is more than 3 days
	elif (mode == "hourly"):
		devices = hourly_repeat + "?siteId=" + str(id) + "&date=" + mainWindow.startdate_entry.get()
	answer = takeRequest(url, devices, username, password)
	return (answer)

# def repeat(id, url, password, username, mainWindow, mode, date): ## if 3 days hours
# 	if (mode == "daily"):
# 		devices = daily_repeat + "?siteId=" + str(id) + "&startDate=" + mainWindow.startdate_entry.get() + "&endDate=" + mainWindow.enddate_entry.get() ##if period is more than 3 days
# 	elif (mode == "hourly"):
# 		devices = hourly_repeat + "?siteId=" + str(id) + "&date=" + date
# 	answer = takeRequest(url, devices, username, password)
# 	return (answer)

# def takeDwellTime(id, url, password, username, mainWindow):
# 	devices = dwell + mainWindow.day + "?siteId=" + str(id)
# 	# print(devices)
# 	answer = takeRequest(url, devices, username, password)
# 	# print(answer)
# 	return (list(answer.values()))

# def takeavDwellTime(id, url, password, username, mainWindow):
# 	devices = av_dwell + mainWindow.day + "?siteId=" + str(id)
# 	# print(devices)
# 	answer = takeRequest(url, devices, username, password)
# 	# print(answer)
# 	return (round(answer))

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

# def testsumvisitors(id, url, password, usernamem, mainWindow):
# 	devices = test + "?siteId=" + str(id) + "&startDate=" + mainWindow.start_date + "&endDate=" + mainWindow.end_date
# 	# print(devices)
# 	answer = takeRequest(url, devices, username, password)
# 	print(answer)
# 	# return (answer)
