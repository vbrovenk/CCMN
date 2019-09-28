import requests
import json

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

		self.connected = "/api/presence/v1/connected/total"
		self.visitors = "/api/presence/v1/visitor/total"
		self.passerby = "/api/presence/v1/passerby/total"
		self.unique = "/api/presence/v1/visitor/count"

		self.dwell = "/api/presence/v1/dwell/count"
		self.average_dwell = "/api/presence/v1/dwell/average"

		self.insights = "/api/presence/v1/insights"
		self.hourly = "/api/presence/v1/visitor/hourly"
	
	def takeRequest(self, restAPI):
		if restAPI == "/api/location/v2/clients":
			endpoint = self.urlCMX + restAPI
		else:
			endpoint = self.url + restAPI
		# enpoint = self.urlCMX + restAPI if restAPI == "/api/location/v2/clients" else self.url + restAPI
		# print("Try URL: " + endpoint)
		data = None
		try:
			if restAPI == "/api/location/v2/clients":
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


	def takeDwellTime(self, startDate, endDate, mode):
		if (mode == "dwell"):
			devices = self.dwell + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
		elif (mode == "average_dwell"):
			devices = self.average_dwell + "?siteId=" + str(self.id) + "&startDate=" + startDate + "&endDate=" + endDate
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
	
	def takeData(self, dataType, startDate, endDate):
		if (startDate == endDate):
			request = '/api/presence/v1/' + dataType + '/hourly?siteId=' + str(self.id) + '&date=' + startDate
		else:
			request = '/api/presence/v1/' + dataType + '/daily?siteId=' + str(self.id) + '&startDate=' + startDate + '&endDate=' + endDate # if period is more than a day
		return(self.takeRequest(request))

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
		return (answer)