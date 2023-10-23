import sys, math
from typing import Dict, List
from functools import partial
from PyQt6 import QtCore
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt6.QtGui import QIntValidator,QFont

from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout

from package.widgets.button import Buttons
from package.util import constant
from package.service.general_service import get_length, set_buttons_state, layout, perform_transformation
from package.exception.exception import Invalid_Input_Exception, No_Available_Graphics_Exception, Transform_On_Vertex_Exception


class Actions:
	do = []
	redo = []

	@classmethod
	def update_list(cls, action: str, target_dict: Dict):
		cls.do.append({action : len(target_dict) - 1})
		cls.redo.clear()

	@classmethod
	def undo_action(cls):
		if len(cls.do) == 0:
			return
		last_action: Dict[str, int] = cls.do[-1]
		action, index = next(iter(last_action.items()))
		cls.do.remove(last_action)
		if action == 'Dot':
			cls.redo.append({action: Dot.Dots[index]})
			del Dot.Dots[index]
		elif action == 'Line':
			cls.redo.append({action: Line.Lines[index]})
			del Line.Lines[index]
		elif action == 'Square':
			cls.redo.append({action: Quadrilateral.Square[index]})
			del Quadrilateral.Square[index]
		elif action == 'Rectangle':
			cls.redo.append({action: Quadrilateral.Rectangle[index]})
			del Quadrilateral.Rectangle[index]
		elif action == 'Circle':
			cls.redo.append({action: Circle.Circles[index]})
			del Circle.Circles[index]
		elif action == 'Triangle':
			cls.redo.append({action: Triangle.Triangles[index]})
			del Triangle.Triangles[index]

	@classmethod
	def redo_action(cls):
		if len(cls.redo) == 0:
			return
		prev_undo: Dict[str, Dict] = cls.redo[-1]
		action, obj = next(iter(prev_undo.items()))
		cls.redo.remove(prev_undo)
		if action == 'Dot':
			Dot.Dots.update({len(Dot.Dots):obj})
			cls.do.append({action: len(Dot.Dots)-1})
		elif action == 'Line':
			Line.Lines.update({len(Line.Lines):obj})
			cls.do.append({action: len(Line.Lines)-1})
		elif action == 'Square':
			Quadrilateral.Square.update({len(Quadrilateral.Square):obj})
			cls.do.append({action: len(Quadrilateral.Square)-1})
		elif action == 'Rectangle':
			Quadrilateral.Rectangle.update({len(Quadrilateral.Rectangle):obj})
			cls.do.append({action: len(Quadrilateral.Rectangle)-1})
		elif action == 'Circle':
			Circle.Circles.update({len(Circle.Circles):obj})
			cls.do.append({action: len(Circle.Circles)-1})
		elif action == 'Triangle':
			Triangle.Triangles.update({len(Triangle.Triangles):obj})
			cls.do.append({action: len(Triangle.Triangles)-1})


class Dot(QWidget):

	def __init__(self, button: QPushButton):
		super().__init__()
		self.button = button
		self.button_is_checked = False

	def the_button_was_toggled(self, checked):
		self.button_is_checked = checked
		self.draw_dots()

	DOT: bool = False
	DOT_x, DOT_y = None,  None
	Dots: Dict = {}

	@classmethod
	def enable_draw_dot(cls):
		cls.DOT = True
		cls.DOT_x, cls.DOT_y = None,  None

	@classmethod
	def disable_draw_dot(cls):
		cls.DOT = False
		cls.DOT_x, cls.DOT_y = None,  None

	def draw_dots(self):
		if self.button_is_checked:
			self.enable_draw_dot()
			set_buttons_state(self.button.text())
		else:
			self.disable_draw_dot()
			set_buttons_state(self.button.text(), True)


class Line(QWidget):

	def __init__(self, button: QPushButton):
		super().__init__()
		self.button = button
		self.button_is_checked = False

	def the_button_was_toggled(self, checked):
		self.button_is_checked = checked
		self.draw_lines()

	LINE: bool = False
	start_p, end_p = None, None
	Lines: Dict[int, Dict] = {}

	@classmethod
	def enable_draw_line(cls):
		cls.LINE = True
		cls.start_p, cls.end_p = None, None

	@classmethod
	def disable_draw_line(cls):
		cls.LINE = False
		cls.start_p, cls.end_p = None, None


	def draw_lines(self):
		if self.button_is_checked:
			self.enable_draw_line()
			set_buttons_state(self.button.text())
		else:
			self.disable_draw_line()
			set_buttons_state(self.button.text(), True)


class Quadrilateral(QWidget):

	def __init__(self, button: QPushButton):
		super().__init__()
		self.button = button
		self.button_is_checked = False


	def the_button_was_toggled(self, checked):
		self.button_is_checked = checked
		self.draw()

	QUAD: bool = False
	start_p, end_p = None, None
	mode: str = ""
	Rectangle: Dict[int, Dict] = {}
	Square: Dict[int, Dict] = {}

	@classmethod
	def enable_draw(cls):
		cls.QUAD = True
		cls.start_p, cls.end_p = None, None

	@classmethod
	def disable_draw(cls):
		cls.QUAD = False
		cls.start_p, cls.end_p = None, None

	@classmethod
	def set_current_quad(cls, mode: str):
		cls.mode = mode

	def draw(self):
		if self.button_is_checked:
			self.enable_draw()
			set_buttons_state(self.button.text())
			if self.button.text() == constant.BUTTON_LABLE_SQUARE:
				self.set_current_quad("square")
			elif self.button.text() == constant.BUTTON_LABLE_RECTANGLE:
				self.set_current_quad("rectangle")
		else:
			self.disable_draw()
			set_buttons_state(self.button.text(), True)


	def get_top_left_bottom_right_p(start_p: QPoint, end_p: QPoint, square = False):
		top_left: QPoint = None
		bottom_right: QPoint = None
		if start_p.x() < end_p.x() and start_p.y() > end_p.y():
			top_left = QPoint(start_p.x(), end_p.y())
			bottom_right = QPoint(end_p.x(), start_p.y())
		elif start_p.x() > end_p.x() and start_p.y() > end_p.y():
			top_left = end_p
			bottom_right = start_p
		elif start_p.x() > end_p.x() and start_p.y() < end_p.y():
			top_left = QPoint(end_p.x(), start_p.y())
			bottom_right = QPoint(start_p.x(), end_p.y())
		else:
			top_left = start_p
			bottom_right = end_p

		return top_left, bottom_right


class Circle(QWidget):

	def __init__(self, button: QPushButton):
		super().__init__()
		self.button = button
		self.button_is_checked = False

	def the_button_was_toggled(self, checked):
		self.button_is_checked = checked
		self.draw_circle()

	CIRCLE: bool = False
	central, circle_p = None, None
	Circles: Dict[int, Dict] = {}

	@classmethod
	def enable_draw_circle(cls):
		cls.CIRCLE = True
		cls.central, cls.circle_p = None, None

	@classmethod
	def disable_draw_circle(cls):
		cls.CIRCLE = False
		cls.central, cls.circle_p = None, None


	def draw_circle(self):
		if self.button_is_checked:
			self.enable_draw_circle()
			set_buttons_state(self.button.text())
		else:
			self.disable_draw_circle()
			set_buttons_state(self.button.text(), True)


class Triangle(QWidget):

	def __init__(self, button: QPushButton):
		super().__init__()
		self.button = button
		self.button_is_checked = False

	def the_button_was_toggled(self, checked):
		self.button_is_checked = checked
		self.draw_triangle()

	TRIANGEL: bool = False
	vertecies = []
	Triangles: Dict[int, Dict] = {}

	@classmethod
	def enable_draw_triangle(cls):
		cls.TRIANGEL = True
		cls.vertecies.clear()

	@classmethod
	def disable_draw_triangle(cls):
		cls.TRIANGEL = False
		cls.vertecies.clear()


	def draw_triangle(self):
		if self.button_is_checked:
			self.enable_draw_triangle()
			set_buttons_state(self.button.text())
		else:
			self.disable_draw_triangle()
			set_buttons_state(self.button.text(), True)


class Transformer(QWidget):
	def __init__(self, window_title: str):
		parent = None
		super(Transformer, self).__init__(parent)
		self.setWindowTitle(window_title)
		self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
		self.config_window(window_title)
		self.show()

	def config_window(self, window_title):
		l = QFormLayout()

		confirm = QPushButton()
		confirm.setText("OK")
		confirm.setFont(QFont('Arial', 20))
		confirm.clicked.connect(partial(self.matrix_formation, window_title))

		if window_title == "Move":
			self.x_inputBox, self.y_inputBox = QLineEdit(), QLineEdit()
			self.x_inputBox.setValidator(QIntValidator())
			self.y_inputBox.setValidator(QIntValidator())
			self.x_inputBox.setMaxLength(3)
			self.y_inputBox.setMaxLength(3)
			
			l.addRow("x variance",self.x_inputBox)
			l.addRow("y variance",self.y_inputBox)
			l.addRow(confirm)
		elif window_title == "Rotate":
			self.theta_inputBox = QLineEdit()
			self.theta_inputBox.setValidator(QIntValidator())
			self.theta_inputBox.setMaxLength(3)

			l.addRow("rotate theta",self.theta_inputBox)
			l.addRow(confirm)
		elif window_title == "Scale":
			self.x_scale, self.y_scale = QLineEdit(), QLineEdit()
			self.x_scale.setValidator(QIntValidator())
			self.y_scale.setValidator(QIntValidator())
			self.x_scale.setMaxLength(2)
			self.y_scale.setMaxLength(2)

			l.addRow("x scale",self.x_scale)
			l.addRow("y scale",self.y_scale)
			l.addRow(confirm)

		self.setLayout(l)


	def matrix_formation(self, window_title):
		try:
			self.matrix = []
			if window_title == "Move":
				self.matrix = [\
						[1, 0, int(self.x_inputBox.text())], \
						[0, 1, int(self.y_inputBox.text())], \
						[0, 0, 1]]
			elif window_title == "Rotate":
				degree = ((360 - int(self.theta_inputBox.text()))*(math.pi/180))
				self.matrix = [\
						[round(math.cos(degree), 1), (-1) * round(math.sin(degree), 1), 0], \
						[round(math.sin(degree), 1), round(math.cos(degree), 1), 0], \
						[0, 0, 1]]
			elif window_title == "Scale":
				self.matrix = [\
						[int(self.x_scale.text()), 0, 0], \
						[0, int(self.y_scale.text()), 0], \
						[0, 0, 1]]
			self.close()
			self.transform(window_title)
		except Exception as e:
			Invalid_Input_Exception(str(e))
			pass

	def transform(self, window_title):
		try:
			last_action: Dict[str, int] = Actions.do[-1]
			action, index = next(iter(last_action.items()))
			if action == 'Dot':
				try:
					if not window_title == "Move":
						self.matrix = None
					new = perform_transformation(self.matrix, [Dot.Dots[index]["x"], Dot.Dots[index]["y"], 1])
					Dot.Dots.update({ index: {"x": new.x(), "y": new.y(), "color": Dot.Dots[index]["color"]} })
				except Exception as e:
					Transform_On_Vertex_Exception()
					pass
			elif action == 'Line':
				if not window_title == "Move":
					print(window_title)
					start_p, end_p = perform_transformation(self.matrix, [Line.Lines[index]["start_p"].x(), Line.Lines[index]["start_p"].y(), 1], [Line.Lines[index]["start_p"].x(), Line.Lines[index]["start_p"].y()]), \
									perform_transformation(self.matrix, [Line.Lines[index]["end_p"].x(), Line.Lines[index]["end_p"].y(), 1], [Line.Lines[index]["start_p"].x(), Line.Lines[index]["start_p"].y()])
				else:
					start_p, end_p = perform_transformation(self.matrix, [Line.Lines[index]["start_p"].x(), Line.Lines[index]["start_p"].y(), 1]), \
									perform_transformation(self.matrix, [Line.Lines[index]["end_p"].x(), Line.Lines[index]["end_p"].y(), 1])
				Line.Lines.update({ index: {"start_p": start_p,  "end_p": end_p,  "color": Line.Lines[index]["color"]} })
			elif action == 'Square':
				p1, p2, p4, p3 = Quadrilateral.Square[index]["vertecies"][0], Quadrilateral.Square[index]["vertecies"][1], \
								Quadrilateral.Square[index]["vertecies"][2], Quadrilateral.Square[index]["vertecies"][3]
				edge = get_length(p1, p2)
				if not window_title == "Move":
					new1, new2, new4, new3 = \
							perform_transformation(self.matrix, [p1.x(), p1.y(), 1], [p1.x(), p1.y()]), \
							perform_transformation(self.matrix, [p2.x(), p2.y(), 1], [p1.x(), p1.y()]), \
							perform_transformation(self.matrix, [p4.x(), p4.y(), 1], [p1.x(), p1.y()]), \
							perform_transformation(self.matrix, [p3.x(), p3.y(), 1], [p1.x(), p1.y()])
				else:
					new1, new2, new4, new3 = \
							perform_transformation(self.matrix, [p1.x(), p1.y(), 1]), \
							perform_transformation(self.matrix, [p2.x(), p2.y(), 1]), \
							perform_transformation(self.matrix, [p4.x(), p4.y(), 1]), \
							perform_transformation(self.matrix, [p3.x(), p3.y(), 1])
				Quadrilateral.Square.update({ index: {"vertecies": [new1, new2, new4, new3],  "color": Quadrilateral.Square[index]["color"]} })
			elif action == 'Rectangle':
				p1, p2, p4, p3 = Quadrilateral.Rectangle[index]["vertecies"][0], Quadrilateral.Rectangle[index]["vertecies"][1], \
								Quadrilateral.Rectangle[index]["vertecies"][2], Quadrilateral.Rectangle[index]["vertecies"][3]
				width, height = get_length(p1, p2), get_length(p2, p3)
				if not window_title == "Move":
					new1, new2, new4, new3 = \
							perform_transformation(self.matrix, [p1.x(), p1.y(), 1], [p1.x(), p1.y()]), \
							perform_transformation(self.matrix, [p2.x(), p2.y(), 1], [p1.x(), p1.y()]), \
							perform_transformation(self.matrix, [p4.x(), p4.y(), 1], [p1.x(), p1.y()]), \
							perform_transformation(self.matrix, [p3.x(), p3.y(), 1], [p1.x(), p1.y()])
				else:
					new1, new2, new4, new3 = \
							perform_transformation(self.matrix, [p1.x(), p1.y(), 1]), \
							perform_transformation(self.matrix, [p2.x(), p2.y(), 1]), \
							perform_transformation(self.matrix, [p4.x(), p4.y(), 1]), \
							perform_transformation(self.matrix, [p3.x(), p3.y(), 1])
				Quadrilateral.Rectangle.update({ index: {"vertecies": [new1, new2, new4, new3],  "color": Quadrilateral.Rectangle[index]["color"]} })
			elif action == 'Circle':
				central = Circle.Circles[index]['central']
				p = QPoint(Circle.Circles[index]['central'].x() + Circle.Circles[index]['radius'], Circle.Circles[index]['central'].y())
				if not window_title == "Move":
					new_central, p = perform_transformation(self.matrix, [central.x(), central.y(), 1], [central.x(), central.y(), 1]), \
									perform_transformation(self.matrix, [p.x(), p.y(), 1], [central.x(), central.y(), 1])
				else:
					new_central, p = perform_transformation(self.matrix, [central.x(), central.y(), 1]), \
									perform_transformation(self.matrix, [p.x(), p.y(), 1])
				Circle.Circles.update({ index: {"central": new_central,  "radius": get_length(new_central, p),  "color": Circle.Circles[index]["color"]} })
			elif action == 'Triangle':
				p1, p2, p3 = Triangle.Triangles[index]["vertecies"][0], Triangle.Triangles[index]["vertecies"][1], \
								Triangle.Triangles[index]["vertecies"][2]
				if not window_title == "Move":
					new1, new2, new3 = \
							perform_transformation(self.matrix, [p1.x(), p1.y(), 1], [p1.x(), p1.y()]), \
							perform_transformation(self.matrix, [p2.x(), p2.y(), 1], [p1.x(), p1.y()]), \
							perform_transformation(self.matrix, [p3.x(), p3.y(), 1], [p1.x(), p1.y()])
				else:
					new1, new2, new3 = \
							perform_transformation(self.matrix, [p1.x(), p1.y(), 1]), \
							perform_transformation(self.matrix, [p2.x(), p2.y(), 1]), \
							perform_transformation(self.matrix, [p3.x(), p3.y(), 1])
				Triangle.Triangles.update({ index: {"vertecies": [new1, new2, new3], "color": Triangle.Triangles[index]["color"]} })

		except Exception as e:
			No_Available_Graphics_Exception(str(e))
			pass









