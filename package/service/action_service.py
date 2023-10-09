import sys
from typing import Dict, List
from PyQt6 import QtCore
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton

from package.widgets.button import Buttons
from package.util import constant
from package.service.general_service import set_buttons_state


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
	Lines: Dict[QPoint, QPoint] = {}

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
	Rectangle: Dict[QPoint, List] = {}
	Square: Dict[QPoint, float] = {}

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











