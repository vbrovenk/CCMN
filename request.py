import requests
import json
import os
from PIL import ImageTk, Image
import shutil

# TODO: rename file to request

class Request:
	def __init__(self):
		self.urlCMX = "https://cisco-cmx.unit.ua"
		self.usernameCMX = "RO"
		self.passwordCMX = "just4reading"
		# TODO: check crashes with incorrect credentials
		self.url = "https://cisco-presence.unit.ua"
		self.username = "RO"
		self.password = "Passw0rd"

		self.id = self.takeSiteId()
		self.imgNames = []

		# SBASNAKA TODO: move these attributes to functions where they are used
		self.connected = "/api/presence/v1/connected/total"
		self.visitors = "/api/presence/v1/visitor/total"
		self.passerby = "/api/presence/v1/passerby/total"
		self.unique = "/api/presence/v1/visitor/count"

		self.dwell = "/api/presence/v1/dwell/count"
		self.dwell_average = "/api/presence/v1/dwell/average"

		self.insights = "/api/presence/v1/insights"
		self.hourly = "/api/presence/v1/visitor/hourly"
	
	def takeRequest(self, restAPI):
		if restAPI == "/api/location/v2/clients" or restAPI == "/api/config/v1/maps":
			endpoint = self.urlCMX + restAPI
		else:
			endpoint = self.url + restAPI
		# enpoint = self.urlCMX + restAPI if restAPI == "/api/location/v2/clients" else self.url + restAPI
		# print("Try URL: " + endpoint)
		# SBASNAKA TODO: finish or remove
		data = None
		try:
			if restAPI == "/api/location/v2/clients" or restAPI == "/api/config/v1/maps":
				returnData = requests.request("GET", endpoint, auth=(self.usernameCMX, self.passwordCMX), verify=False)
			else:
				returnData = requests.request("GET", endpoint, auth=(self.username, self.password), verify=False)
			data = json.loads(returnData.text)
		except Exception as e:
			print(e)
		return (data)

	def takeTotalVisitors(self, startDate, endDate, mode):
		if (mode == "connected"):
			devices = self.connected + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (mode == "visitors"):
			devices = self.visitors + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (mode == "passerby"):
			devices = self.passerby + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		else:
			devices = self.unique + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		answer = self.takeRequest(devices)
		return answer


	def takeDwellTime(self, startDate, endDate, mode):
		if (mode == "dwell"):
			devices = self.dwell + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (mode == "dwell_average"):
			devices = self.dwell_average + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		answer = self.takeRequest(devices)
		return answer


	def takeInsights(self, startDate, endDate, mode):
		if (mode == "month_peakhour"):
			devices = self.insights + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (startDate == endDate and mode == "day_peakhour"):
			devices = self.hourly + "?siteId=" + str(self.id) + "&date=" + startDate
		answer = self.takeRequest(devices)
		return answer

	def takeCooords(self):
		location = None
		try:
			location = self.takeRequest("/api/location/v2/clients")
		except Exception as e:
			print(e)
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
		return(self.takeRequest(request))

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
		return(self.takeRequest(request))

	def takeSiteId(self):
		data = self.takeRequest("/api/config/v1/sites")
		id = data[0]["aesUId"]
		return (id)

	def getFloorImage(self):
		mapdatajson = self.takeRequest("/api/config/v1/maps")
		mapImages = []
		try:
			os.mkdir("./maps")
			# TODO: remove /maps from git
		except OSError:
			print("Creation of the directory is failed")
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
						print(e)

		self.resizeImgs()

	def resizeImgs(self):
		width = 1280
		height = 720

		im1 = Image.open("maps/" + self.imgNames[0])
		im5 = im1.resize((width, height), Image.ANTIALIAS)
		im5.save("maps/1stFloor" + ".jpg")

		im1 = Image.open("maps/" + self.imgNames[2])
		im5 = im1.resize((width, height), Image.ANTIALIAS)
		im5.save("maps/2ndFloor" + ".jpg")

		im1 = Image.open("maps/" + self.imgNames[1])
		im5 = im1.resize((width, height), Image.ANTIALIAS)
		im5.save("maps/3rdFloor" + ".jpg")
