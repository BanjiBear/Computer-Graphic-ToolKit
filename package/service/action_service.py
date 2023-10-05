import sys
from typing import Dict
from PyQt6 import QtCore
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton

from package.widgets.button import Buttons
from package.service.general_service import set_buttons_state


class Dot(QWidget):

	def __init__(self, button: QPushButton):
		super().__init__()
		self.button = button
		self.button_is_checked = False

	def the_button_was_toggled(self, checked):
		self.button_is_checked = checked
		print(self.button_is_checked)
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
			print("On!")
		else:
			self.disable_draw_dot()
			set_buttons_state(self.button.text(), True)
			print("Off")


class Line(QWidget):

	def __init__(self, button: QPushButton):
		super().__init__()
		self.button = button
		self.button_is_checked = False

	def the_button_was_toggled(self, checked):
		self.button_is_checked = checked
		print(self.button_is_checked)
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
			print("On!")
		else:
			self.disable_draw_line()
			set_buttons_state(self.button.text(), True)
			print("Off")













