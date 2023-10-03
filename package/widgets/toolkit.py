import sys
from enum import Enum
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget

from package.util import constant
from package.util.util import EnvSetting
from package.widgets.button import Buttons
from package.service.action_service import ActionsService


class PremitiveTools(Enum):
	Dot = constant.BUTTON_LABLE_DOT
	Line = constant.BUTTON_LABLE_LINE
	Square = constant.BUTTON_LABLE_SQUARE
	Rectangle = constant.BUTTON_LABLE_RECTANGLE
	Circle = constant.BUTTON_LAYOUT_CIRCLE
	Triangle = constant.BUTTON_LABLE_TRIANGLE
	Arrow = constant.BUTTON_LABLE_ARROW


class ToolKit(QWidget):

	def __init__(self, canvas):
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

		self.canvas = canvas

		self.setWindowTitle(EnvSetting.ENV[constant.TOOLKIT_TITLE])
		self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

		self.toolkit_width, self.toolkit_height = int(EnvSetting.ENV[constant.TOOLKIT__WIDTH]), int(EnvSetting.ENV[constant.TOOLKIT__HEIGHT])
		if self.toolkit_width == 0 or self.toolkit_height == 0:
			screen = self.canvas.app.primaryScreen()
			self.toolkit_width, self.toolkit_height = screen.size().width() * 0.15, screen.size().height()
		self.resize(self.toolkit_width, self.toolkit_height)


	def create_primitive_tools(self):
		self.buttons = Buttons(self.toolkit_width, self.toolkit_height)
		label = [i.value for i in PremitiveTools]
		self.buttons.create_button(label)

		self.set_primitve_tools_action()

		layout = EnvSetting.ENV[constant.BUTTON_LAYOUT]
		self.setLayout(self.buttons.button_layout(layout))

		self.show()



