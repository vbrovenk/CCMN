import requests
import json
import os
from PIL import ImageTk, Image
from PIL import ImageTk, Image
import shutil

# TODO: rename file to Request

class Request:
	def __init__(self):
		self.urlCMX = "https://cisco-cmx.unit.ua"
		self.usernameCMX = "RO"
		self.passwordCMX = "just4reading"

		self.url = "https://cisco-presence.unit.ua"
		self.username = "RO"
		self.password = "Passw0rd"

		self.id = self.takeSiteId()
		self.imgNames = []

		self.connected = "/api/presence/v1/connected/total"
		self.visitors = "/api/presence/v1/visitor/total"
		self.passerby = "/api/presence/v1/passerby/total"
		self.unique = "/api/presence/v1/visitor/count"

		self.daily_connected_graph = "/api/presence/v1/connected/daily"
		self.daily_visitors_graph = "/api/presence/v1/visitor/daily"
		self.daily_passerby_graph = "/api/presence/v1/passerby/daily"

		self.hourly_connected_graph = "/api/presence/v1/connected/hourly"
		self.hourly_visitors_graph = "/api/presence/v1/visitor/hourly"
		self.hourly_passerby_graph = "/api/presence/v1/passerby/hourly"

		self.dwell = "/api/presence/v1/dwell/count"
		self.average_dwell = "/api/presence/v1/dwell/average"

		self.daily_dwelltime_graph = "/api/presence/v1/dwell/daily"
		self.hourly_dwelltime_graph = "/api/presence/v1/dwell/hourly"

		self.insights = "/api/presence/v1/insights"
		self.hourly = "/api/presence/v1/visitor/hourly"
	
	def takeRequest(self, restAPI):
		if restAPI == "/api/location/v2/clients" or restAPI == "/api/config/v1/maps":
			endpoint = self.urlCMX + restAPI
		else:
			endpoint = self.url + restAPI
		# enpoint = self.urlCMX + restAPI if restAPI == "/api/location/v2/clients" else self.url + restAPI
		# print("Try URL: " + endpoint)
		data = None
		try:
			if restAPI == "/api/location/v2/clients" or restAPI == "/api/config/v1/maps":
				returnData = requests.request("GET", endpoint, auth=(self.usernameCMX, self.passwordCMX), verify=False)
			else:
				returnData = requests.request("GET", endpoint, auth=(self.username, self.password), verify=False)
			# print(json.dumps(returnData, indent = 5))
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

	def takeTotalVisitorsGraph(self, startDate, endDate):
		answer = []
		if (startDate == endDate):
			connected = self.hourly_connected_graph + "?siteId=" + str(self.id) + "&date=" + startDate
			visitors = self.hourly_visitors_graph + "?siteId=" + str(self.id) + "&date=" + startDate
			passerby = self.hourly_passerby_graph + "?siteId=" + str(self.id) + "&date=" + startDate
		elif (mode == "hourly"):
			connected = self.daily_connected_graph + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
			visitors = self.daily_visitors_graph + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
			passerby = self.daily_passerby_graph + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		answer.append(self.takeRequest(connected))
		answer.append(self.takeRequest(visitors))
		answer.append(self.takeRequest(passerby))
		return answer

	def takeDwellTime(self, startDate, endDate, mode):
		if (mode == "dwell"):
			devices = self.dwell + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (mode == "average_dwell"):
			devices = self.average_dwell + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		answer = self.takeRequest(devices)
		return answer

	def takeDwellTimeGraph(self, startDate, endDate):
		if (startDate == endDate):
			devices = self.hourly_dwelltime_graph + "?siteId=" + str(self.id) + "&date=" + startDate
		else:
			devices = self.daily_dwelltime_graph + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		answer = self.takeRequest(devices)
		return answer

	def takeInsights(self, startDate, endDate, mode):
		if (mode == "month_peakhour"):
			devices = self.insights + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (startDate == endDate and mode == "day_peakhour"):
			devices = self.hourly + "/" + "?siteId=" + str(self.id) + "&date=" + startDate
		answer = self.takeRequest(devices)
		return answer

	def takeCooords(self):
		location = None
		try:
			location = self.takeRequest("/api/location/v2/clients")
			# print(json.dumps(location, indent = 5))
		except Exception as e:
			print(e)
		return (location)
	
	def takeSiteId(self):
		data = self.takeRequest("/api/config/v1/sites")
		id = data[0]["aesUId"]
		return (id)

	def takeRepeatVisitors(self, startDate, endDate):
		if (startDate == endDate):
			devices = "/api/presence/v1/repeatvisitors/hourly?siteId=" + str(self.id) + "&date=" + startDate
		else:
			devices = "/api/presence/v1/repeatvisitors/daily?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate # if period is more than a day
		answer = self.takeRequest(devices)
		return (answer)= endDate):
			devices = "/api/presence/v1/repeatvisitors/hourly?siteId=" + str(self.id) + "&date=" + startDate
		else:
			devices = "/api/presence/v1/repeatvisitors/daily?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate # if period is more than a day
		answer = self.takeRequest(devices)
		return (answer)

	def getFloorImage(self):
		mapdatajson = self.takeRequest("/api/config/v1/maps")
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

					endpoint = self.urlCMX + \
					"/api/config/v1/maps/imagesource/" + \
					floor["image"]["imageName"]

					print("trying " + endpoint)
					try:
						response = requests.request("GET", endpoint, \
						auth=(self.usernameCMX, self.passwordCMX), stream=True, verify=False)
						print("Got Map")

						with open("./maps/" + \
						floor["image"]["imageName"], 'wb') as f:
							self.imgNames.append(floor["image"]["imageName"])
							response.raw.decode_content = True
							shutil.copyfileobj(response.raw, f)
					except Exception as e:
						print(e)
		# print (self.imgNames)
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