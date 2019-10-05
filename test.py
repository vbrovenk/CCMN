import urllib3
from window import Window
from request import Request

# TODO: rename file + update README

def main():
	###### GUI ######
	urllib3.disable_warnings()

	###### CLASS ########
	# test = cisco.Request()
	# test.getFloorImage() # TODO SBASNAKA: just test, but need to do it before passing project!!!
	mainWindow = Window(Request())
	mainWindow.start()		

if __name__ == "__main__":
	main()