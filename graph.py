from cisco import Request

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

class Graph:

	def __init__(self, tab, tabName):
		self.canvas = None
		self.request = Request()
		self.tab = tab
		self.tabName = tabName

		# self.tab = event.widget #event.widget.tab(event.widget.select(), "text")
	# def changeTab(self, event):
	# 	self.tab = event.widget
	# 	self.tabName = event.widget.tab(event.widget.select(), 'text')
	# 	print(self.tabName)

	def show(self, startDate, endDate):

		fig, graph = plt.subplots(figsize=(10,5))

		# OSAMOILE TODO: change colors and legend similar to https://cisco-presence.unit.ua/presence/
		# OSAMOILE TODO: resolve crash with mouse scroll

		if (self.tabName == 'Repeat Visitors'):
			data = self.request.takeData('repeatvisitors', startDate, endDate)
			keys = list(data.keys())
			xaxis = np.arange(len(keys)) # put bars side to side

			DAILY = [data.get(key).get('DAILY') for key in keys]
			WEEKLY = [data.get(key).get('WEEKLY') for key in keys]
			OCCASIONAL = [data.get(key).get('OCCASIONAL') for key in keys]
			FIRST_TIME = [data.get(key).get('FIRST_TIME') for key in keys]
			YESTERDAY = [data.get(key).get('YESTERDAY') for key in keys]

			graph.bar(xaxis - 0.3, DAILY, width=0.15, label='DAILY')
			graph.bar(xaxis - 0.15, WEEKLY, width=0.15, label='WEEKLY')
			graph.bar(xaxis, OCCASIONAL, width=0.15, label='OCCASIONAL')
			graph.bar(xaxis + 0.15, FIRST_TIME, width=0.15, label='FIRST_TIME')
			graph.bar(xaxis + 0.3, YESTERDAY, width=0.15, label='YESTERDAY')

		elif (self.tabName == 'Dwell Time'):
			data = self.request.takeData('dwell', startDate, endDate)
			keys = list(data.keys())
			xaxis = np.arange(len(keys)) # put bars side to side

			FIVE_TO_THIRTY_MINUTES = [data.get(key).get('FIVE_TO_THIRTY_MINUTES') for key in keys]
			THIRTY_TO_SIXTY_MINUTES = [data.get(key).get('THIRTY_TO_SIXTY_MINUTES') for key in keys]
			ONE_TO_FIVE_HOURS = [data.get(key).get('ONE_TO_FIVE_HOURS') for key in keys]
			FIVE_TO_EIGHT_HOURS = [data.get(key).get('FIVE_TO_EIGHT_HOURS') for key in keys]
			EIGHT_PLUS_HOURS = [data.get(key).get('EIGHT_PLUS_HOURS') for key in keys]

			graph.bar(xaxis - 0.3, FIVE_TO_THIRTY_MINUTES, width=0.15, label='FIVE_TO_THIRTY_MINUTES')
			graph.bar(xaxis - 0.15, THIRTY_TO_SIXTY_MINUTES, width=0.15, label='THIRTY_TO_SIXTY_MINUTES')
			graph.bar(xaxis, ONE_TO_FIVE_HOURS, width=0.15, label='ONE_TO_FIVE_HOURS')
			graph.bar(xaxis + 0.15, FIVE_TO_EIGHT_HOURS, width=0.15, label='FIVE_TO_EIGHT_HOURS')
			graph.bar(xaxis + 0.3, EIGHT_PLUS_HOURS, width=0.15, label='EIGHT_PLUS_HOURS')

		elif (self.tabName == 'Proximity'):
			connected = self.request.takeData('connected', startDate, endDate)
			visitors = self.request.takeData('visitor', startDate, endDate)
			passerby = self.request.takeData('passerby', startDate, endDate)
			keys = list(connected.keys())
			xaxis = np.arange(len(keys)) # put bars side to side

			CONNECTED = [connected.get(key) for key in keys]
			VISITORS = [visitors.get(key) for key in keys]
			PASSERBY = [passerby.get(key) for key in keys]
			
			graph.bar(xaxis - 0.15, CONNECTED, width=0.15, label='CONNECTED')
			graph.bar(xaxis, VISITORS, width=0.15, label='VISITORS')
			graph.bar(xaxis + 0.15, PASSERBY, width=0.15, label='PASSERBY')

		if (self.canvas):
			self.canvas.get_tk_widget().destroy() # othervise graphics are stacking
		graph.set_xticks(xaxis)
		graph.set_xticklabels(keys, rotation=45, fontsize=7)
		fig.legend(loc='upper right')
		self.canvas = FigureCanvasTkAgg(fig, master=self.tab)
		self.canvas.get_tk_widget().pack()

		# TODO: Forecasting number of visitors (tomorrow)

		# OSAMOILE TODO: pie chart session duration and the day of the week