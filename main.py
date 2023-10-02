import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow


from package.widgets.toolkit import ToolKit
from package.util import constant
from package.util.util import EnvSetting



class Canvas(QMainWindow):

	def __init__(self):
		self.app = QApplication([])

		super().__init__()
		self.setWindowTitle(EnvSetting.ENV[constant.CANVAS_TITLE])

		if int(EnvSetting.ENV[constant.CANVAS_WIDTH]) == 0 or int(EnvSetting.ENV[constant.CANVAS_HEIGHT]) == 0:
			screen = self.app.primaryScreen()
			# geometry = screen.availableGeometry()
			self.setGeometry(0, 0, screen.size().width(), screen.size().height())
			# self.setFixedSize(geometry.width(), geometry.height())
		else:
			self.setGeometry(0, 0, int(EnvSetting.ENV[constant.CANVAS_WIDTH]), int(EnvSetting.ENV[constant.CANVAS_HEIGHT]))

		self.show()

	def init_toolkit(self):
		self.toolkit = ToolKit()
		self.toolkit.createToolKit(self.app)

		self.toolkit.create_button()

		self.toolkit.show()




if __name__ == "__main__":

	# System Setting
	EnvSetting.read_env_file("./env/prd.env")
	
	# Initialize the Tool Kit
	canvas = Canvas()
	canvas.init_toolkit()

	# Run
	sys.exit(canvas.app.exec())






