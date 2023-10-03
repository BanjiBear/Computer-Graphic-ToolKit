from typing import Dict, List
from enum import Enum
from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout

from package.util import constant
from package.util.util import EnvSetting


class Layout(Enum):
	QHBoxLayout = QHBoxLayout()
	QVBoxLayout = QVBoxLayout()
	QGridLayout = QGridLayout()
	QFormLayout = QFormLayout()


class Buttons:

	buttons: Dict[str, QPushButton] = {}

	def __init__(self, toolkit_width, toolkit_height):
		self.toolkit_width = toolkit_width
		self.toolkit_height = toolkit_height

	def create_button(self, button_label : List):
		for lable in button_label:
			button = QPushButton()
			button.setText(lable)
			button.setFont(QFont('Arial', 30))
			button.setFixedSize(QtCore.QSize(40, 40))
			# Reference: https://stackoverflow.com/questions/56975249/button-resizing-automatically
			self.update_buttons(button)
			# print(button.text())

	@classmethod
	def update_buttons(cls, button):
		cls.buttons.update({button.text():button})


	def button_layout(self, layout: str):
		self.layout = Layout[layout].value
		self.layout.setSpacing(10)
		self.layout.setContentsMargins(0, 0, 0, 0)
		# Reference: https://stackoverflow.com/questions/67563632/how-to-reduce-the-space-between-two-widgets-in-pyqt5-qgridlayout#:~:text=To%20remove%20the%20space%20between,to%20the%20imaginary%20fifth%20column.

		if layout == "QGridLayout":
			x = 0
			y = 0
			for b in self.buttons:
				if y >= int(EnvSetting.ENV[constant.NUMBER_OF_BUTTONS_IN_ROW]):
					x = x + 1
					y = 0
				# print(x, y, buttons[b].text())
				self.layout.addWidget(self.buttons[b], x, y)
				y = y + 1
		elif layout == "QFormLayout":
			# layout.addRow(b for b in tmp)
			...
		else:
			self.layout.addStretch(1)
			for b in self.buttons:
				self.layout.addWidget(self.buttons[b])

		return self.layout




