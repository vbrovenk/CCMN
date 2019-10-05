from window import Window
from request import Request

import urllib3

if __name__ == "__main__":
	urllib3.disable_warnings()
	# TODO SBASNAKA: just test, but need to do it before passing project!!!
	# TODO SBASNAKA: remove maps/ from git. time to deal with it!
	# test = cisco.Request()
	# test.getFloorImage()
	mainWindow = Window(Request())
	mainWindow.start()