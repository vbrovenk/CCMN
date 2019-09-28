import cisco
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

class Graph:

	def __init__(self, tab):
		self.canvas = None
		self.request = cisco.Request()
		self.tab = tab

	def show(self, startDate, endDate):
		data = self.request.takeRepeatVisitors(startDate, endDate)
		# print(data)

		keys = list(data.keys())
		daily = [data.get(hour).get('DAILY') for hour in keys]				# list of DAILY values for every hour
		weekly = [data.get(hour).get('WEEKLY') for hour in keys]			# list of WEEKLY values for every hour
		occasional = [data.get(hour).get('OCCASIONAL') for hour in keys]	# list of OCCASIONAL values for every hour
		first_time = [data.get(hour).get('FIRST_TIME') for hour in keys]	# list of FIRST_TIME values for every hour
		yesterday = [data.get(hour).get('YESTERDAY') for hour in keys]		# list of YESTERDAY values for every hour

		xaxis = np.arange(len(keys)) # put bars side to side

		fig, graph = plt.subplots(figsize=(10,5))
		graph.bar(xaxis - 0.3, daily, width=0.15, label='DAILY')
		graph.bar(xaxis - 0.15, weekly, width=0.15, label='WEEKLY')
		graph.bar(xaxis, occasional, width=0.15, label='OCCASIONAL')
		graph.bar(xaxis + 0.15, first_time, width=0.15, label='FIRST_TIME')
		graph.bar(xaxis + 0.3, yesterday, width=0.15, label='YESTERDAY')
		# OSAMOILE TODO: change x-axis

		if (self.canvas):
			self.canvas.get_tk_widget().destroy()

		fig.legend(loc='upper right')
		self.canvas = FigureCanvasTkAgg(fig, master=self.tab)
		self.canvas.get_tk_widget().pack()

		# TODO: Forecasting number of visitors (tomorrow)

		# OSAMOILE TODO: session duration and the day of the week
		#       number of connections and the day of the week