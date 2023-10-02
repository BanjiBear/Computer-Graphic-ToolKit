from typing import List
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


class Button:

	def __init__(self, toolkit_width, toolkit_height):
		self.toolkit_width = toolkit_width
		self.toolkit_height = toolkit_height

	def create_button(self, layout: str, button_label : List):
		button_list = []
		self.layout = Layout[layout].value
		self.layout.setSpacing(10)
		self.layout.setContentsMargins(0, 0, 0, 0)
		# Reference: https://stackoverflow.com/questions/67563632/how-to-reduce-the-space-between-two-widgets-in-pyqt5-qgridlayout#:~:text=To%20remove%20the%20space%20between,to%20the%20imaginary%20fifth%20column.
		
		for lable in button_label:
			button = QPushButton()
			button.setText(lable)
			button.setFont(QFont('Arial', 30))
			button.setFixedSize(QtCore.QSize(40, 40))
			# Reference: https://stackoverflow.com/questions/56975249/button-resizing-automatically
			button_list.append(button)
			# print(button.text())

		if layout == "QGridLayout":
			x = 0
			y = 0
			for b in button_list:
				if y >= int(EnvSetting.ENV[constant.NUMBER_OF_BUTTONS_IN_ROW]):
					x = x + 1
					y = 0
				# print(x, y, b.text())
				self.layout.addWidget(b, x, y)
				y = y + 1
		elif layout == "QFormLayout":
			patch = 0
			for i in len(button_list) / int(EnvSetting.ENV[constant.NUMBER_OF_BUTTONS_IN_ROW]):
				...
				layout.addRow(b for b in tmp)
		else:
			self.layout.addStretch(1)
			for b in button_list:
				self.layout.addWidget(b)

		return self.layout




