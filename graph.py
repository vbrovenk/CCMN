from request import Request

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import calendar

# SBASNAKA TODO: current month as default
# SBASNAKA TODO: startDate is week ago as default

class Graph:

	def __init__(self, tab, tabName):
		self.canvas = None
		self.request = Request()
		self.tab = tab
		self.tabName = tabName

	def __makeForecast(self):
		period = (datetime.datetime.today() - relativedelta(months = 2)).strftime("%Y-%m-%d")
		tommorow_weekday = (datetime.datetime.today() + datetime.timedelta(days = 1)).strftime("%A")
		today = datetime.datetime.today().strftime("%Y-%m-%d")

		connected = self.request.takeDailyData('connected', period, today)
		visitors = self.request.takeDailyData('visitor', period, today)
		passerby = self.request.takeDailyData('passerby', period, today)
		dwell = self.request.takeDailyData('dwell', period, today)
		repeat = self.request.takeDailyData('repeatvisitors', period, today)
		
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

	def __preparePie(self, pieData, pie):
		pieDict = dict()
		for value in pieData:
			date = datetime.datetime.strptime(value['date'], '%Y-%m-%d')
			day = calendar.day_name[date.weekday()] # date.weekday returns number of a day
			if (day not in pieDict):
				pieDict.update({day:0})
			pieDict[day] = pieDict[day] + value['count']
		pie.pie(pieDict.values(), labels=pieDict.values(),
			shadow=True, explode=[0.1] * len(pieDict))
		pie.legend(pieDict.keys(), loc='upper right')

	def __prepareRepeatVisitorsGraph(self, bars, pie, forecast, startDate, endDate):
		if (startDate == endDate):
			data = self.request.takeHourlyData('repeatvisitors', startDate)
		else:
			data = self.request.takeDailyData('repeatvisitors', startDate, endDate)

		DAILY = [data.get(key).get('DAILY') for key in data.keys()]
		WEEKLY = [data.get(key).get('WEEKLY') for key in data.keys()]
		OCCASIONAL = [data.get(key).get('OCCASIONAL') for key in data.keys()]
		FIRST_TIME = [data.get(key).get('FIRST_TIME') for key in data.keys()]
		YESTERDAY = [data.get(key).get('YESTERDAY') for key in data.keys()]

		labels = list(data.keys())
		if (startDate != endDate):
			xaxis = np.arange(len(labels) + 1) # +1 for prediction
			DAILY.append(forecast['DAILY'])
			WEEKLY.append(forecast['WEEKLY'])
			OCCASIONAL.append(forecast['OCCASIONAL'])
			FIRST_TIME.append(forecast['FIRST_TIME'])
			YESTERDAY.append(forecast['YESTERDAY'])
			tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # today plus one day
			labels.append(tomorrow)
		else:
			xaxis = np.arange(len(labels))
			data = self.request.takeDailyData('repeatvisitors', startDate, endDate) # for pie
		
		pieData = [dict(date=key, count=data.get(key).get('DAILY')) for key in data.keys()]
		pie.set_title('Daily')
		self.__preparePie(pieData, pie)

		bars.bar(xaxis - 0.3, DAILY, width=0.15, label='Daily')
		bars.bar(xaxis - 0.15, WEEKLY, width=0.15, label='Weekly')
		bars.bar(xaxis, OCCASIONAL, width=0.15, label='Occasional')
		bars.bar(xaxis + 0.15, FIRST_TIME, width=0.15, label='First Time')
		bars.bar(xaxis + 0.3, YESTERDAY, width=0.15, label='Yesterday')
		return labels, xaxis

	def __prepareDwellTimeGraph(self, bars, pie, forecast, startDate, endDate):
		if (startDate == endDate):
			data = self.request.takeHourlyData('dwell', startDate)
		else:
			data = self.request.takeDailyData('dwell', startDate, endDate)

		FIVE_TO_THIRTY_MINUTES = [data.get(key).get('FIVE_TO_THIRTY_MINUTES') for key in data.keys()]
		THIRTY_TO_SIXTY_MINUTES = [data.get(key).get('THIRTY_TO_SIXTY_MINUTES') for key in data.keys()]
		ONE_TO_FIVE_HOURS = [data.get(key).get('ONE_TO_FIVE_HOURS') for key in data.keys()]
		FIVE_TO_EIGHT_HOURS = [data.get(key).get('FIVE_TO_EIGHT_HOURS') for key in data.keys()]
		EIGHT_PLUS_HOURS = [data.get(key).get('EIGHT_PLUS_HOURS') for key in data.keys()]

		labels = list(data.keys())
		if (startDate != endDate):
			xaxis = np.arange(len(labels) + 1) # +1 for prediction
			FIVE_TO_THIRTY_MINUTES.append(forecast['FIVE_TO_THIRTY_MINUTES'])
			THIRTY_TO_SIXTY_MINUTES.append(forecast['THIRTY_TO_SIXTY_MINUTES'])
			ONE_TO_FIVE_HOURS.append(forecast['ONE_TO_FIVE_HOURS'])
			FIVE_TO_EIGHT_HOURS.append(forecast['FIVE_TO_EIGHT_HOURS'])
			EIGHT_PLUS_HOURS.append(forecast['EIGHT_PLUS_HOURS'])
			tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # today plus one day
			labels.append(tomorrow)
		else:
			xaxis = np.arange(len(labels))
			data = self.request.takeDailyData('dwell', startDate, endDate) # for pie

		pieData = [dict(date=key, count=data.get(key).get('EIGHT_PLUS_HOURS')) for key in data.keys()]
		pie.set_title('8+ hours')
		self.__preparePie(pieData, pie)

		bars.bar(xaxis - 0.3, FIVE_TO_THIRTY_MINUTES, width=0.15, label='5-30 mins')
		bars.bar(xaxis - 0.15, THIRTY_TO_SIXTY_MINUTES, width=0.15, label='30-60 mins')
		bars.bar(xaxis, ONE_TO_FIVE_HOURS, width=0.15, label='1-5 hours')
		bars.bar(xaxis + 0.15, FIVE_TO_EIGHT_HOURS, width=0.15, label='5-8 hours')
		bars.bar(xaxis + 0.3, EIGHT_PLUS_HOURS, width=0.15, label='8+ hours')

		return labels, xaxis

	def __prepareProximityGraph(self, bars, pie, forecast, startDate, endDate):
		if (startDate == endDate):
			connected = self.request.takeHourlyData('connected', startDate)
			visitors = self.request.takeHourlyData('visitor', startDate)
			passerby = self.request.takeHourlyData('passerby', startDate)
		else:
			connected = self.request.takeDailyData('connected', startDate, endDate)
			visitors = self.request.takeDailyData('visitor', startDate, endDate)
			passerby = self.request.takeDailyData('passerby', startDate, endDate)

		CONNECTED = [connected.get(key) for key in connected.keys()]
		VISITORS = [visitors.get(key) for key in connected.keys()]
		PASSERBY = [passerby.get(key) for key in connected.keys()]
		
		labels = list(connected.keys())
		if (startDate != endDate):
			xaxis = np.arange(len(labels) + 1) # +1 for prediction
			CONNECTED.append(forecast['CONNECTED'])
			VISITORS.append(forecast['VISITORS'])
			PASSERBY.append(forecast['PASSERBY'])
			tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # today plus one day
			labels.append(tomorrow)
		else:
			xaxis = np.arange(len(labels))
			connected = self.request.takeDailyData('connected', startDate, endDate) # for pie

		pieData = [dict(date=key, count=connected.get(key)) for key in connected.keys()]
		pie.set_title('Connected')
		self.__preparePie(pieData, pie)

		bars.bar(xaxis - 0.15, CONNECTED, width=0.15, label='Connected')
		bars.bar(xaxis, VISITORS, width=0.15, label='Visitors')
		bars.bar(xaxis + 0.15, PASSERBY, width=0.15, label='Passerby')

		return labels, xaxis

	def show(self, startDate, endDate):

		fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,5))

		bars = axes[0]
		pie = axes[1]

		# OSAMOILE TODO: resolve crash with mouse scroll

		forecast = self.__makeForecast() # TODO: why 3 times ?

		if (self.tabName == 'Repeat Visitors'):
			labels, xaxis = self.__prepareRepeatVisitorsGraph(bars, pie, forecast, startDate, endDate)
		elif (self.tabName == 'Dwell Time'):
			labels, xaxis = self.__prepareDwellTimeGraph(bars, pie, forecast, startDate, endDate)
		elif (self.tabName == 'Proximity'):
			labels, xaxis = self.__prepareProximityGraph(bars, pie, forecast, startDate, endDate)

		if (self.canvas):
			self.canvas.get_tk_widget().destroy() # othervise graphics are stacking
		if (startDate == endDate): # TODO: why here ?
			labels = [hour + ':00' for hour in labels]
		bars.set_xticks(xaxis)
		bars.set_xticklabels(labels, rotation=45, fontsize=7)
		if (startDate != endDate):
			bars.get_xticklabels()[len(labels) - 1].set_color('red')
		bars.legend(loc='upper right') # TODO: legend position
		self.canvas = FigureCanvasTkAgg(fig, master=self.tab)
		self.canvas.get_tk_widget().pack()
