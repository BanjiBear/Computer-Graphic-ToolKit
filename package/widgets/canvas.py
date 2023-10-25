import sys, random
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QPainter, QPen, QPolygon, QColor
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow

from package.util import constant
from package.util.util import EnvSetting
from package.widgets.toolkit import ToolKit
from package.service.action_service import Actions, Dot, Line, Quadrilateral, Circle, Triangle
from package.service.general_service import get_edge, get_length


class Canvas(QMainWindow):

	def __init__(self):
		self.app = QApplication([])

		super().__init__()
		self.setWindowTitle(EnvSetting.ENV[constant.CANVAS_TITLE])
		self.setStyleSheet("background-color:" + constant.CANVAS_COLOR + ";")
		if int(EnvSetting.ENV[constant.CANVAS_WIDTH]) == 0 or int(EnvSetting.ENV[constant.CANVAS_HEIGHT]) == 0:
			screen = self.app.primaryScreen()
			self.setGeometry(0, 0, screen.size().width(), screen.size().height())
		else:
			self.setGeometry(0, 0, int(EnvSetting.ENV[constant.CANVAS_WIDTH]), int(EnvSetting.ENV[constant.CANVAS_HEIGHT]))
		self.show()

		# Initialize the Tool Kit
		self.toolkit = ToolKit()

	def closeEvent(self, event):
		event.ignore()



	def mousePressEvent(self, event):
		self.update()
		if Dot.DOT:
			Dot.DOT_x, Dot.DOT_y = event.pos().x(), event.pos().y()
			Dot.Dots.update(\
				{len(Dot.Dots):\
					{"x": Dot.DOT_x, \
					"y": Dot.DOT_y, \
					"color": self.toolkit.current_color}\
				})
			Actions.update_list("Dot", Dot.Dots)
		elif Line.LINE:
			Line.start_p = event.pos()
		elif Quadrilateral.QUAD:
			Quadrilateral.start_p = event.pos()
		elif Circle.CIRCLE:
			Circle.central = event.pos()
		elif Triangle.TRIANGEL:
			Triangle.vertecies.append(event.pos())
			if len(Triangle.vertecies) == 3:
				Triangle.Triangles.update(\
					{len(Triangle.Triangles):\
						{"vertecies": Triangle.vertecies, \
						"color": self.toolkit.current_color}\
					})
				Triangle.vertecies = []
				Actions.update_list("Triangle", Triangle.Triangles)

	def mouseReleaseEvent(self, event):
		self.update()
		if Line.LINE:
			Line.end_p = event.pos()
			Line.Lines.update(\
				{len(Line.Lines):\
					{"start_p": Line.start_p, \
					"end_p": Line.end_p, \
					"color": self.toolkit.current_color}\
				})
			Actions.update_list("Line", Line.Lines)
		elif Quadrilateral.QUAD:
			Quadrilateral.end_p = event.pos()
			if Quadrilateral.mode == "square":
				Quadrilateral.start_p, Quadrilateral.end_p = Quadrilateral.get_top_left_bottom_right_p(Quadrilateral.start_p, Quadrilateral.end_p, True)
				edge = min(get_edge(Quadrilateral.start_p, Quadrilateral.end_p))
				Quadrilateral.Square.update(\
							{len(Quadrilateral.Square):\
								{"vertecies": 
									[Quadrilateral.start_p,\
									QPoint(Quadrilateral.start_p.x() + edge, Quadrilateral.start_p.y()),\
									QPoint(Quadrilateral.start_p.x() + edge, Quadrilateral.start_p.y() + edge),\
									QPoint(Quadrilateral.start_p.x(), Quadrilateral.start_p.y() + edge)],\
								"color": self.toolkit.current_color}\
							})
				Actions.update_list("Square", Quadrilateral.Square)
			elif Quadrilateral.mode == "rectangle":
				Quadrilateral.start_p, Quadrilateral.end_p = Quadrilateral.get_top_left_bottom_right_p(Quadrilateral.start_p, Quadrilateral.end_p)
				width, height = get_edge(Quadrilateral.start_p, Quadrilateral.end_p)
				Quadrilateral.Rectangle.update(\
							{len(Quadrilateral.Rectangle):\
								{"vertecies": 
									[Quadrilateral.start_p,\
									QPoint(Quadrilateral.start_p.x() + width, Quadrilateral.start_p.y()),\
									QPoint(Quadrilateral.start_p.x() + width, Quadrilateral.start_p.y() + height),\
									QPoint(Quadrilateral.start_p.x(), Quadrilateral.start_p.y() + height)],\
								"color": self.toolkit.current_color}\
							})
				Actions.update_list("Rectangle", Quadrilateral.Rectangle)
		elif Circle.CIRCLE:
			Circle.circle_p = event.pos()
			radius = get_length(Circle.central, Circle.circle_p)
			Circle.Circles.update(\
							{len(Circle.Circles):\
								{"central": Circle.central,\
								"radius": radius,\
								"color": self.toolkit.current_color}\
							})
			Actions.update_list("Circle", Circle.Circles)



	def paintEvent(self, event):
		QMainWindow.paintEvent(self, event)
		self.update()

		painter = QPainter()
		painter.begin(self)
		pen = QtGui.QPen()
		pen.setWidth(3)
		
		for d in Dot.Dots:
			pen.setColor(QColor(Dot.Dots[d]['color']))
			painter.setPen(pen)
			painter.drawPoint(Dot.Dots[d]['x'], Dot.Dots[d]['y'])
		for l in Line.Lines:
			pen.setColor(QColor(Line.Lines[l]['color']))
			painter.setPen(pen)
			painter.drawLine(Line.Lines[l]['start_p'], Line.Lines[l]['end_p'])
		for sq in Quadrilateral.Square:
			pen.setColor(QColor(Quadrilateral.Square[sq]['color']))
			painter.setPen(pen)
			painter.drawPolygon(QPolygon(Quadrilateral.Square[sq]['vertecies']))
		for rec in Quadrilateral.Rectangle:
			pen.setColor(QColor(Quadrilateral.Rectangle[rec]['color']))
			painter.setPen(pen)
			painter.drawPolygon(QPolygon(Quadrilateral.Rectangle[rec]['vertecies']))
		for c in Circle.Circles:
			pen.setColor(QColor(Circle.Circles[c]['color']))
			painter.setPen(pen)
			painter.drawEllipse(Circle.Circles[c]['central'].x() - Circle.Circles[c]['radius'], \
							Circle.Circles[c]['central'].y() - Circle.Circles[c]['radius'], \
							Circle.Circles[c]['radius'] * 2, Circle.Circles[c]['radius'] * 2)
		for tri in Triangle.Triangles:
			pen.setColor(QColor(Triangle.Triangles[tri]['color']))
			painter.setPen(pen)
			painter.drawPolygon(QPolygon(Triangle.Triangles[tri]['vertecies']))
		
		painter.end()





