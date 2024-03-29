import requests
import json
import os
from PIL import ImageTk, Image
import shutil
import logging

class Request:
	logging.basicConfig(filename = "log", filemode = "w", format = "%(asctime)s - %(levelname)s - %(message)s", datefmt = "%d/%m/%Y %I:%M:%S", level = logging.INFO)
	def __init__(self):
		self.urlCMX = "https://cisco-cmx.unit.ua"
		self.usernameCMX = "RO"
		self.passwordCMX = "just4reading"

		self.url = "https://cisco-presence.unit.ua"
		self.username = "RO"
		self.password = "Passw0rd"

		self.id = self.takeSiteId()
		self.imgNames = []

	def takeRequest(self, restAPI):
		if restAPI == "/api/location/v2/clients" or restAPI == "/api/config/v1/maps":
			endpoint = self.urlCMX + restAPI
		else:
			endpoint = self.url + restAPI
		data = None
		try:
			if restAPI == "/api/location/v2/clients" or restAPI == "/api/config/v1/maps":
				returnData = requests.request("GET", endpoint, auth=(self.usernameCMX, self.passwordCMX), verify=False)
			else:
				returnData = requests.request("GET", endpoint, auth=(self.username, self.password), verify=False)
			data = json.loads(returnData.text)
			logging.info("Successfuly made request")
		except Exception as e:
			logging.error("takeRequest: " + str(e))
		return (data)

	def takeTotalVisitors(self, startDate, endDate, mode):
		if (mode == "connected"):
			devices = "/api/presence/v1/connected/total" + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (mode == "visitors"):
			devices = "/api/presence/v1/visitor/total" + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (mode == "passerby"):
			devices = "/api/presence/v1/passerby/total" + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		else:
			devices = "/api/presence/v1/visitor/count" + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		answer = self.takeRequest(devices)
		return answer


	def takeDwellTime(self, startDate, endDate, mode):
		if (mode == "dwell"):
			devices = "/api/presence/v1/dwell/count" + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (mode == "dwell_average"):
			devices = "/api/presence/v1/dwell/average" + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		answer = self.takeRequest(devices)
		return answer


	def takeInsights(self, startDate, endDate, mode):
		if (mode == "month_peakhour"):
			devices = "/api/presence/v1/insights" + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (startDate == endDate and mode == "day_peakhour"):
			devices = "/api/presence/v1/visitor/hourly" + "?siteId=" + str(self.id) + "&date=" + startDate
		answer = self.takeRequest(devices)
		return answer

	def takeCooords(self):
		location = None
		try:
			location = self.takeRequest("/api/location/v2/clients")
		except Exception as e:
			logging.error("takeCoords: " + str(e))
		return (location)

	def takeHourlyData(self, dataType, date):
		'''
			List of suitable data types:
				* repeatvisitors
				* dwell
				* connected
				* visitor
				* passerby
				* mb etc but not used
		'''
		request = '/api/presence/v1/' + dataType + '/hourly?siteId=' + str(self.id) + '&date=' + date
		data = self.takeRequest(request)
		data = { key:value for key,value in data.items() if value is not None}
		return data

	def takeDailyData(self, dataType, startDate, endDate):
		'''
			List of suitable data types:
				* repeatvisitors
				* dwell
				* connected
				* visitor
				* passerby
				* mb etc but not used
		'''
		request = '/api/presence/v1/' + dataType + '/daily?siteId=' + str(self.id) + '&startDate=' + startDate + '&endDate=' + endDate # if period is more than a day
		data = self.takeRequest(request)
		data = { key:value for key,value in data.items() if value is not None}
		return data

	def takeSiteId(self):
		data = self.takeRequest("/api/config/v1/sites")
		if data is not None:
			id = data[0]["aesUId"]
			logging.info("Successfuly took sites id")
			return (id)
		else:
			logging.error('Check your internet connection')
			exit()

	def getFloorImage(self):
		mapdatajson = self.takeRequest("/api/config/v1/maps")
		if not mapdatajson:
			logging.error('Check your internet connection')
			exit()
		mapImages = []
		try:
			os.mkdir("./maps")
			logging.info("Successfuly created directory for the maps")
		except OSError as e:
			pass
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

					endpoint = self.urlCMX + \
					"/api/config/v1/maps/imagesource/" + \
					floor["image"]["imageName"]

					try:
						response = requests.request("GET", endpoint, \
						auth=(self.usernameCMX, self.passwordCMX), stream=True, verify=False)
						with open("./maps/" + \
						floor["image"]["imageName"], 'wb') as f:
							self.imgNames.append(floor["image"]["imageName"])
							response.raw.decode_content = True
							shutil.copyfileobj(response.raw, f)
					except Exception as e:
						pass
		logging.info("Successfuly downloaded images of the maps")
		self.resizeImgs()

	def resizeImgs(self):
		width = 1280
		height = 720

		name = "maps/" + self.imgNames[0]
		img = Image.open(name)
		img = img.resize((width, height), Image.ANTIALIAS)
		img.save(name)
		os.rename(name, "maps/1stFloor" + ".jpg")

		name = "maps/" + self.imgNames[2]
		img = Image.open(name)
		img = img.resize((width, height), Image.ANTIALIAS)
		img.save(name)
		os.rename(name, "maps/2ndFloor" + ".jpg")

		name = "maps/" + self.imgNames[1]
		img = Image.open(name)
		img = img.resize((width, height), Image.ANTIALIAS)
		img.save(name)
		os.rename(name, "maps/3rdFloor" + ".jpg")
