import urllib3

from window import Window
import cisco

def createGUI():
	###### CLASS ########
	# test = cisco.Request()
	# test.getFloorImage() #######just test, but need to do it before passing project!!!
	mainWindow = Window()
	mainWindow.start()
	# mainWindow.window.mainloop()

def main():
	###### GUI ######
	urllib3.disable_warnings()
	createGUI()

if __name__ == "__main__":
	main()