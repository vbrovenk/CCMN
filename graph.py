from cisco import Request

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import datetime

class Graph:

	def __init__(self, tab, tabName):
		self.canvas = None
		self.request = Request()
		self.tab = tab
		self.tabName = tabName

	def predict3(self):
		return [ 50, 100, 150 ]

	def predict5(self):
		return [ 50, 100, 150, 200, 250 ]

	def __prepareRepeatVisitorsGraph(self, graph, startDate, endDate):
		data = self.request.takeData('repeatvisitors', startDate, endDate)

		keys = list(data.keys())
		if (startDate != endDate):
			xaxis = np.arange(len(keys) + 1) # +1 for prediction
		else:
			xaxis = np.arange(len(keys))

		DAILY = [data.get(key).get('DAILY') for key in keys]
		WEEKLY = [data.get(key).get('WEEKLY') for key in keys]
		OCCASIONAL = [data.get(key).get('OCCASIONAL') for key in keys]
		FIRST_TIME = [data.get(key).get('FIRST_TIME') for key in keys]
		YESTERDAY = [data.get(key).get('YESTERDAY') for key in keys]

		if (startDate != endDate):
			forecast = self.predict5()
			DAILY.append(forecast[0])
			WEEKLY.append(forecast[1])
			OCCASIONAL.append(forecast[2])
			FIRST_TIME.append(forecast[3])
			YESTERDAY.append(forecast[4])
			tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # today plus one day
			keys.append(tomorrow)

		graph.bar(xaxis - 0.3, DAILY, width=0.15, label='DAILY')
		graph.bar(xaxis - 0.15, WEEKLY, width=0.15, label='WEEKLY')
		graph.bar(xaxis, OCCASIONAL, width=0.15, label='OCCASIONAL')
		graph.bar(xaxis + 0.15, FIRST_TIME, width=0.15, label='FIRST_TIME')
		graph.bar(xaxis + 0.3, YESTERDAY, width=0.15, label='YESTERDAY')

		return keys, xaxis

	def __prepareDwellTimeGraph(self, graph, startDate, endDate):
		data = self.request.takeData('dwell', startDate, endDate)

		keys = list(data.keys())
		if (startDate != endDate):
			xaxis = np.arange(len(keys) + 1) # +1 for prediction
		else:
			xaxis = np.arange(len(keys))

		FIVE_TO_THIRTY_MINUTES = [data.get(key).get('FIVE_TO_THIRTY_MINUTES') for key in keys]
		THIRTY_TO_SIXTY_MINUTES = [data.get(key).get('THIRTY_TO_SIXTY_MINUTES') for key in keys]
		ONE_TO_FIVE_HOURS = [data.get(key).get('ONE_TO_FIVE_HOURS') for key in keys]
		FIVE_TO_EIGHT_HOURS = [data.get(key).get('FIVE_TO_EIGHT_HOURS') for key in keys]
		EIGHT_PLUS_HOURS = [data.get(key).get('EIGHT_PLUS_HOURS') for key in keys]

		if (startDate != endDate):
			forecast = self.predict5()
			FIVE_TO_THIRTY_MINUTES.append(forecast[0])
			THIRTY_TO_SIXTY_MINUTES.append(forecast[1])
			ONE_TO_FIVE_HOURS.append(forecast[2])
			FIVE_TO_EIGHT_HOURS.append(forecast[3])
			EIGHT_PLUS_HOURS.append(forecast[4])
			tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # today plus one day
			keys.append(tomorrow)

		graph.bar(xaxis - 0.3, FIVE_TO_THIRTY_MINUTES, width=0.15, label='FIVE_TO_THIRTY_MINUTES')
		graph.bar(xaxis - 0.15, THIRTY_TO_SIXTY_MINUTES, width=0.15, label='THIRTY_TO_SIXTY_MINUTES')
		graph.bar(xaxis, ONE_TO_FIVE_HOURS, width=0.15, label='ONE_TO_FIVE_HOURS')
		graph.bar(xaxis + 0.15, FIVE_TO_EIGHT_HOURS, width=0.15, label='FIVE_TO_EIGHT_HOURS')
		graph.bar(xaxis + 0.3, EIGHT_PLUS_HOURS, width=0.15, label='EIGHT_PLUS_HOURS')

		return keys, xaxis

	def __prepareProximityGraph(self, graph, startDate, endDate):
		connected = self.request.takeData('connected', startDate, endDate)
		visitors = self.request.takeData('visitor', startDate, endDate)
		passerby = self.request.takeData('passerby', startDate, endDate)

		keys = list(connected.keys())
		if (startDate != endDate):
			xaxis = np.arange(len(keys) + 1) # +1 for prediction
		else:
			xaxis = np.arange(len(keys))

		CONNECTED = [connected.get(key) for key in keys]
		VISITORS = [visitors.get(key) for key in keys]
		PASSERBY = [passerby.get(key) for key in keys]
		
		if (startDate != endDate):
			forecast = self.predict3()
			CONNECTED.append(forecast[0])
			VISITORS.append(forecast[1])
			PASSERBY.append(forecast[2])
			tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # today plus one day
			keys.append(tomorrow)

		graph.bar(xaxis - 0.15, CONNECTED, width=0.15, label='CONNECTED')
		graph.bar(xaxis, VISITORS, width=0.15, label='VISITORS')
		graph.bar(xaxis + 0.15, PASSERBY, width=0.15, label='PASSERBY')

		return keys, xaxis

	def show(self, startDate, endDate):

		fig, graph = plt.subplots(figsize=(10,5))

		# OSAMOILE TODO: change legend similar to https://cisco-presence.unit.ua/presence/
		# OSAMOILE TODO: resolve crash with mouse scroll

		if (self.tabName == 'Repeat Visitors'):
			keys, xaxis = self.__prepareRepeatVisitorsGraph(graph, startDate, endDate)
		elif (self.tabName == 'Dwell Time'):
			keys, xaxis = self.__prepareDwellTimeGraph(graph, startDate, endDate)
		elif (self.tabName == 'Proximity'):
			keys, xaxis = self.__prepareProximityGraph(graph, startDate, endDate)

		if (self.canvas):
			self.canvas.get_tk_widget().destroy() # othervise graphics are stacking
		if (startDate == endDate):
			keys = [hour + ':00' for hour in keys]
		graph.set_xticks(xaxis)
		graph.set_xticklabels(keys, rotation=45, fontsize=7)
		if (startDate != endDate):
			graph.get_xticklabels()[len(keys) - 1].set_color('red') # TODO: need pylint ?
		fig.legend(loc='upper right')
		self.canvas = FigureCanvasTkAgg(fig, master=self.tab)
		self.canvas.get_tk_widget().pack()

		# OSAMOILE TODO: pie chart session duration and the day of the week