import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow

from package.util import constant
from package.util.util import EnvSetting


class Canvas(QMainWindow):

	def __init__(self):

		self.mouseTrackable = False

		self.app = QApplication([])

		super().__init__()
		self.setMouseTracking(self.mouseTrackable)
		self.setWindowTitle(EnvSetting.ENV[constant.CANVAS_TITLE])

		if int(EnvSetting.ENV[constant.CANVAS_WIDTH]) == 0 or int(EnvSetting.ENV[constant.CANVAS_HEIGHT]) == 0:
			screen = self.app.primaryScreen()
			# geometry = screen.availableGeometry()
			self.setGeometry(0, 0, screen.size().width(), screen.size().height())
			# self.setFixedSize(geometry.width(), geometry.height())
		else:
			self.setGeometry(0, 0, int(EnvSetting.ENV[constant.CANVAS_WIDTH]), int(EnvSetting.ENV[constant.CANVAS_HEIGHT]))

		self.show()

	def setMouseTrackable(self, status: bool):
		self.mouseTrackable = status

	def mouseMoveEvent(self, event):
		print(event.pos())