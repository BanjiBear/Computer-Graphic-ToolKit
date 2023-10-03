import sys, random
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow

from package.util import constant
from package.util.util import EnvSetting
from package.service.action_service import Dot, Line


class Canvas(QMainWindow):

	def __init__(self):

		# self.mouseTrackable = False

		self.app = QApplication([])

		super().__init__()
		# self.setMouseTracking(self.mouseTrackable)
		self.setWindowTitle(EnvSetting.ENV[constant.CANVAS_TITLE])

		if int(EnvSetting.ENV[constant.CANVAS_WIDTH]) == 0 or int(EnvSetting.ENV[constant.CANVAS_HEIGHT]) == 0:
			screen = self.app.primaryScreen()
			self.setGeometry(0, 0, screen.size().width(), screen.size().height())
		else:
			self.setGeometry(0, 0, int(EnvSetting.ENV[constant.CANVAS_WIDTH]), int(EnvSetting.ENV[constant.CANVAS_HEIGHT]))

		self.show()

	# def setMouseTrackable(self, status: bool):
	# 	self.mouseTrackable = status
	# 	self.setMouseTracking(self.mouseTrackable)



	def mousePressEvent(self, event):
		self.update()
		if Dot.DOT:
			Dot.DOT_x, Dot.DOT_y = event.pos().x(), event.pos().y()
			Dot.Dots.update({Dot.DOT_x : Dot.DOT_y})
		elif Line.LINE:
			Line.start_p = event.pos()

	def mouseReleaseEvent(self, event):
		self.update()
		if Line.LINE:
			Line.end_p = event.pos()
			Line.Lines.update({Line.start_p : Line.end_p})



	def paintEvent(self, event):
		QMainWindow.paintEvent(self, event)
		self.update()
		if not Dot.DOT_x == None and not Dot.DOT_y == None:
			painter = QPainter()
			painter.begin(self)
			painter.setPen(Qt.GlobalColor.red)
			for x in Dot.Dots:
				painter.drawPoint(x, Dot.Dots[x])
			painter.end()
		elif Line.LINE:
			painter = QPainter()
			painter.begin(self)
			pen = QtGui.QPen()
			pen.setWidth(15)
			pen.setColor(Qt.GlobalColor.red)
			painter.setPen(pen)
			for l in Line.Lines:
				painter.drawLine(l, Line.Lines[l])
			painter.end()





