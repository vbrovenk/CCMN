from window import Window
from request import Request

import urllib3

if __name__ == "__main__":
	urllib3.disable_warnings()
	mainWindow = Window(Request())
	mainWindow.start()