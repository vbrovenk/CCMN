from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta

class Graph:

	def __init__(self, request, tab, tabName):
		self.canvas = None
		self.request = request
		self.tab = tab
		self.tabName = tabName

	def __makeForecast(self):
		period = (datetime.datetime.today() - relativedelta(months = 2)).strftime("%Y-%m-%d")
		tommorow_weekday = (datetime.datetime.today() + datetime.timedelta(days = 1)).strftime("%A")
		today = datetime.datetime.today().strftime("%Y-%m-%d")

		connected = self.request.takeData('connected', period, today)
		visitors = self.request.takeData('visitor', period, today)
		passerby = self.request.takeData('passerby', period, today)
		dwell = self.request.takeData('dwell', period, today)
		repeat = self.request.takeData('repeatvisitors', period, today)
		
		forecast = dict()
		con_list = []
		vis_list = []
		pass_list = []
		dwell_list = []
		repeat_list = []

		for i in connected:
			splited = str(i).split("-")
			date = datetime.date(int(splited[0]), int(splited[1]), int(splited[2]))
			if date.strftime("%A") == tommorow_weekday:
				con_list.append(connected[i])
				vis_list.append(visitors[i])
				pass_list.append(passerby[i])
				dwell_list.append(dwell[i])
				repeat_list.append(repeat[i])

		forecast['CONNECTED'] = round(sum(con_list) / len(con_list))
		forecast['VISITORS'] = round(sum(vis_list) / len(vis_list))
		forecast['PASSERBY'] = round(sum(pass_list) / len(pass_list))

		five_to_thirty = [i['FIVE_TO_THIRTY_MINUTES'] for i in dwell_list]
		thirty_to_sixty = [i['THIRTY_TO_SIXTY_MINUTES'] for i in dwell_list]
		one_to_five = [i['ONE_TO_FIVE_HOURS'] for i in dwell_list]
		five_to_eight = [i['FIVE_TO_EIGHT_HOURS'] for i in dwell_list]
		eight_plus = [i['EIGHT_PLUS_HOURS'] for i in dwell_list]

		forecast['FIVE_TO_THIRTY_MINUTES'] = round(sum(five_to_thirty) / len(five_to_thirty))
		forecast['THIRTY_TO_SIXTY_MINUTES'] = round(sum(thirty_to_sixty) / len(thirty_to_sixty))
		forecast['ONE_TO_FIVE_HOURS'] = round(sum(one_to_five) / len(one_to_five))
		forecast['FIVE_TO_EIGHT_HOURS'] = round(sum(five_to_eight) / len(five_to_eight))
		forecast['EIGHT_PLUS_HOURS'] = round(sum(eight_plus) / len(eight_plus))

		daily = [i['DAILY'] for i in repeat_list]
		weekly = [i['WEEKLY'] for i in repeat_list]
		occasional = [i['OCCASIONAL'] for i in repeat_list]
		first_time = [i['FIRST_TIME'] for i in repeat_list]
		yesterday =[i['YESTERDAY'] for i in repeat_list]

		forecast['DAILY'] = round(sum(daily) / len(daily))
		forecast['WEEKLY'] = round(sum(weekly) / len(weekly))
		forecast['OCCASIONAL'] = round(sum(occasional) / len(occasional))
		forecast['FIRST_TIME'] = round(sum(first_time) / len(first_time))
		forecast['YESTERDAY'] = round(sum(yesterday) / len(yesterday))

		return (forecast)

	def __prepareRepeatVisitorsGraph(self, graph, forecast, startDate, endDate):
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
			DAILY.append(forecast['DAILY'])
			WEEKLY.append(forecast['WEEKLY'])
			OCCASIONAL.append(forecast['OCCASIONAL'])
			FIRST_TIME.append(forecast['FIRST_TIME'])
			YESTERDAY.append(forecast['YESTERDAY'])
			tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # today plus one day
			keys.append(tomorrow)

		graph.bar(xaxis - 0.3, DAILY, width=0.15, label='DAILY')
		graph.bar(xaxis - 0.15, WEEKLY, width=0.15, label='WEEKLY')
		graph.bar(xaxis, OCCASIONAL, width=0.15, label='OCCASIONAL')
		graph.bar(xaxis + 0.15, FIRST_TIME, width=0.15, label='FIRST_TIME')
		graph.bar(xaxis + 0.3, YESTERDAY, width=0.15, label='YESTERDAY')

		return keys, xaxis

	def __prepareDwellTimeGraph(self, graph, forecast, startDate, endDate):
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
			FIVE_TO_THIRTY_MINUTES.append(forecast['FIVE_TO_THIRTY_MINUTES'])
			THIRTY_TO_SIXTY_MINUTES.append(forecast['THIRTY_TO_SIXTY_MINUTES'])
			ONE_TO_FIVE_HOURS.append(forecast['ONE_TO_FIVE_HOURS'])
			FIVE_TO_EIGHT_HOURS.append(forecast['FIVE_TO_EIGHT_HOURS'])
			EIGHT_PLUS_HOURS.append(forecast['EIGHT_PLUS_HOURS'])
			tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # today plus one day
			keys.append(tomorrow)

		graph.bar(xaxis - 0.3, FIVE_TO_THIRTY_MINUTES, width=0.15, label='FIVE_TO_THIRTY_MINUTES')
		graph.bar(xaxis - 0.15, THIRTY_TO_SIXTY_MINUTES, width=0.15, label='THIRTY_TO_SIXTY_MINUTES')
		graph.bar(xaxis, ONE_TO_FIVE_HOURS, width=0.15, label='ONE_TO_FIVE_HOURS')
		graph.bar(xaxis + 0.15, FIVE_TO_EIGHT_HOURS, width=0.15, label='FIVE_TO_EIGHT_HOURS')
		graph.bar(xaxis + 0.3, EIGHT_PLUS_HOURS, width=0.15, label='EIGHT_PLUS_HOURS')

		return keys, xaxis

	def __prepareProximityGraph(self, graph, forecast, startDate, endDate):
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
			CONNECTED.append(forecast['CONNECTED'])
			VISITORS.append(forecast['VISITORS'])
			PASSERBY.append(forecast['PASSERBY'])
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

		forecast = self.__makeForecast()

		if (self.tabName == 'Repeat Visitors'):
			keys, xaxis = self.__prepareRepeatVisitorsGraph(graph, forecast, startDate, endDate)
		elif (self.tabName == 'Dwell Time'):
			keys, xaxis = self.__prepareDwellTimeGraph(graph, forecast, startDate, endDate)
		elif (self.tabName == 'Proximity'):
			keys, xaxis = self.__prepareProximityGraph(graph, forecast, startDate, endDate)

		if (self.canvas):
			self.canvas.get_tk_widget().destroy() # othervise graphics are stacking
		if (startDate == endDate):
			keys = [hour + ':00' for hour in keys]
		graph.set_xticks(xaxis)
		graph.set_xticklabels(keys, rotation=45, fontsize=7)
		if (startDate != endDate):
			graph.get_xticklabels()[len(keys) - 1].set_color('red')
		fig.legend(loc='upper right')
		self.canvas = FigureCanvasTkAgg(fig, master=self.tab)
		self.canvas.get_tk_widget().pack()

		# OSAMOILE TODO: pie chart session duration and the day of the week