import sys
from enum import Enum
from functools import partial
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget

from package.util import constant
from package.util.util import EnvSetting
from package.widgets.button import Buttons
from package.service.action_service import Actions, Dot, Line, Quadrilateral, Circle, Triangle
from package.service.action_service import Transformer
from package.service.general_service import layout

class PremitiveTools(Enum):
	Dot = constant.BUTTON_LABLE_DOT
	Line = constant.BUTTON_LABLE_LINE
	Square = constant.BUTTON_LABLE_SQUARE
	Rectangle = constant.BUTTON_LABLE_RECTANGLE
	Circle = constant.BUTTON_LAYOUT_CIRCLE
	Triangle = constant.BUTTON_LABLE_TRIANGLE

class Colors(Enum):
	Red = "#d00000"
	Blue = "#0000FF"
	Green = "#008000"
	Yellow = "#FFFF00"
	Orange = "#FFA500"
	Black = "#000000"

class Transformations(Enum):
	Translation = "Move"
	Rotation = "Rotate"
	Scaling = "Scale"


class ToolKit(QWidget):

	def __init__(self):
		parent = None
		super(ToolKit, self).__init__(parent)

		"""
		Description: Canvas is a sub-window created by the main window. 
			It is target to stay within the main window
			and Always on top of the main window
		Reference: 
			https://stackoverflow.com/questions/70045339/what-is-analog-of-setwindowflags-in-pyqt6
			https://itecnote.com/tecnote/qt-how-to-put-a-child-window-inside-a-main-windowpyqt/
			https://stackoverflow.com/questions/30470433/how-to-put-a-child-window-inside-a-main-windowpyqt
		"""

		self.setWindowTitle(EnvSetting.ENV[constant.TOOLKIT_TITLE])
		self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

		self.toolkit_width, self.toolkit_height = int(EnvSetting.ENV[constant.TOOLKIT__WIDTH]), int(EnvSetting.ENV[constant.TOOLKIT__HEIGHT])
		# if self.toolkit_width == 0 or self.toolkit_height == 0:
		# 	screen = self.canvas.app.primaryScreen()
		# 	self.toolkit_width, self.toolkit_height = screen.size().width() * 0.15, screen.size().height()
		# self.resize(self.toolkit_width, self.toolkit_height)

		self.buttons = Buttons(self.toolkit_width, self.toolkit_height)
		self.create_primitive_tools(self.buttons)
		self.create_color_palette(self.buttons)
		self.current_color = constant.DEFAULT_COLOR
		self.create_transformation_tools(self.buttons)
		self.create_other_tools(self.buttons)
		self.show()

	def closeEvent(self, event):
		event.ignore()


	def create_primitive_tools(self, buttons):
		# self.buttons = Buttons(self.toolkit_width, self.toolkit_height)
		label = [i.value for i in PremitiveTools]
		self.buttons.create_button(len(label), label, None)

		self.set_primitve_tools_action()

		Layout = EnvSetting.ENV[constant.BUTTON_LAYOUT]
		self.setLayout(layout(Layout, Buttons.buttons))

	def create_color_palette(self, buttons):
		colors = [i.value for i in Colors]
		self.buttons.create_button(len(colors), None, colors)
		self.set_color_palette_action()
		Layout = EnvSetting.ENV[constant.BUTTON_LAYOUT]
		self.setLayout(layout(Layout, Buttons.buttons))

	def create_transformation_tools(self, buttons):
		label = [i.value for i in Transformations]
		self.buttons.create_button(len(label), label, None, 10)
		self.set_transformation_action()
		Layout = EnvSetting.ENV[constant.BUTTON_LAYOUT]
		# addWidget = partial(self.buttons.layout.addWidget, rowSpan = 1, columnSpan = 2)
		self.setLayout(layout(Layout, Buttons.buttons))


	def create_other_tools(self, buttons):
		label = ["undo", "redo", "exit"]
		self.buttons.create_button(len(label), label, None, 15)
		self.set_other_tools_action()
		Layout = EnvSetting.ENV[constant.BUTTON_LAYOUT]
		self.setLayout(layout(Layout, Buttons.buttons))



	def set_primitve_tools_action(self):

		for button in Buttons.buttons:
			Buttons.buttons[button].setCheckable(True)
			if button == constant.BUTTON_LABLE_DOT:
				self.dot = Dot(Buttons.buttons[button])
				Buttons.buttons[button].clicked.connect(self.dot.the_button_was_toggled)
			elif button == constant.BUTTON_LABLE_LINE:
				self.line = Line(Buttons.buttons[button])
				Buttons.buttons[button].clicked.connect(self.line.the_button_was_toggled)
			elif button == constant.BUTTON_LABLE_SQUARE:
				self.square = Quadrilateral(Buttons.buttons[button])
				Buttons.buttons[button].clicked.connect(self.square.the_button_was_toggled)
			elif button == constant.BUTTON_LABLE_RECTANGLE:
				self.rectangle = Quadrilateral(Buttons.buttons[button])
				Buttons.buttons[button].clicked.connect(self.rectangle.the_button_was_toggled)
			elif button == constant.BUTTON_LAYOUT_CIRCLE:
				self.circle = Circle(Buttons.buttons[button])
				Buttons.buttons[button].clicked.connect(self.circle.the_button_was_toggled)
			elif button == constant.BUTTON_LABLE_TRIANGLE:
				self.triangle = Triangle(Buttons.buttons[button])
				Buttons.buttons[button].clicked.connect(self.triangle.the_button_was_toggled)

	def set_color_palette_action(self):
		for button in Buttons.buttons:
			if "color_#" in button:
				Buttons.buttons[button].clicked.connect(partial(self.set_color, button))
				#reference: https://stackoverflow.com/questions/42773709/pyqt5-show-which-button-was-clicked#:~:text=To%20find%20out%20which%20button,were%20added%20to%20the%20group.
				#	1. check which button is clicked, same connect function
				#	2. pass text without arguments

	def set_color(self, color: str):
		# color prefix: "color_"
		self.current_color = color[6:len(color)]



	def set_transformation_action(self):
		for button in Buttons.buttons:
			if button in [i.value for i in Transformations]:
				Buttons.buttons[button].clicked.connect(partial(self.init_transform, button))

	def init_transform(self, transform_type):
		self.transform = Transformer(transform_type)


	def set_other_tools_action(self):
		for button in Buttons.buttons:
			if button == "exit":
				Buttons.buttons[button].clicked.connect(sys.exit)
			elif button == "undo":
				Buttons.buttons[button].clicked.connect(Actions.undo_action)
			elif button == "redo":
				Buttons.buttons[button].clicked.connect(Actions.redo_action)





