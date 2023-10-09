import sys, random
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QPainter, QPen, QPolygon
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow

from package.util import constant
from package.util.util import EnvSetting
from package.service.action_service import Dot, Line, Quadrilateral, Circle, Triangle
from package.service.general_service import get_edge, get_length


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
		elif Quadrilateral.QUAD:
			Quadrilateral.start_p = event.pos()
		elif Circle.CIRCLE:
			Circle.central = event.pos()
		elif Triangle.TRIANGEL:
			Triangle.vertecies.append(event.pos())
			if len(Triangle.vertecies) == 3:
				Triangle.Triangles.append(Triangle.vertecies)
				Triangle.vertecies = []

	def mouseReleaseEvent(self, event):
		self.update()
		if Line.LINE:
			Line.end_p = event.pos()
			Line.Lines.update({Line.start_p : Line.end_p})
		elif Quadrilateral.QUAD:
			Quadrilateral.end_p = event.pos()
			if Quadrilateral.mode == "square":
				Quadrilateral.start_p, Quadrilateral.end_p = Quadrilateral.get_top_left_bottom_right_p(Quadrilateral.start_p, Quadrilateral.end_p, True)
				width, height = get_edge(Quadrilateral.start_p, Quadrilateral.end_p)
				Quadrilateral.Square.update({Quadrilateral.start_p: min(width, height)})
			elif Quadrilateral.mode == "rectangle":
				Quadrilateral.start_p, Quadrilateral.end_p = Quadrilateral.get_top_left_bottom_right_p(Quadrilateral.start_p, Quadrilateral.end_p)
				width, height = get_edge(Quadrilateral.start_p, Quadrilateral.end_p)
				Quadrilateral.Rectangle.update({Quadrilateral.start_p: [width, height]})
		elif Circle.CIRCLE:
			Circle.circle_p = event.pos()
			radius = get_length(Circle.central, Circle.circle_p)
			Circle.Circles.update({Circle.central: radius})



	def paintEvent(self, event):
		QMainWindow.paintEvent(self, event)
		self.update()

		painter = QPainter()
		painter.begin(self)
		pen = QtGui.QPen()
		pen.setColor(Qt.GlobalColor.red)
		pen.setWidth(3)
		painter.setPen(pen)
		
		for x in Dot.Dots:
			painter.drawPoint(x, Dot.Dots[x])
		for l in Line.Lines:
			painter.drawLine(l, Line.Lines[l])
		for sq in Quadrilateral.Square:
			painter.drawRect(sq.x(), sq.y(), Quadrilateral.Square[sq], Quadrilateral.Square[sq])
		for rec in Quadrilateral.Rectangle:
			painter.drawRect(rec.x(), rec.y(), Quadrilateral.Rectangle[rec][0], Quadrilateral.Rectangle[rec][1])
		for c in Circle.Circles:
			painter.drawEllipse(c.x() - Circle.Circles[c], c.y() - Circle.Circles[c], Circle.Circles[c] * 2, Circle.Circles[c] * 2)
		for tri in Triangle.Triangles:
			painter.drawPolygon(QPolygon(tri))
		
		painter.end()





