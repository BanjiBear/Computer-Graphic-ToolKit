from typing import Dict, List
from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QPushButton


class Buttons:

	buttons: Dict[str, QPushButton] = {}

	def __init__(self, toolkit_width, toolkit_height):
		self.toolkit_width = toolkit_width
		self.toolkit_height = toolkit_height

	def create_button(self, number_of_buttons: int, button_label : List, colors: List, fontsize = 40, size = [50,50]):
		for i in range(number_of_buttons):
			button = QPushButton()
			if button_label:
				button.setText(button_label[i])
				button.setFont(QFont('Arial', fontsize))
			if colors:
				button.setStyleSheet("background-color:" + colors[i] + ";")
			button.setFixedSize(QtCore.QSize(size[0], size[1]))
			# Reference: https://stackoverflow.com/questions/56975249/button-resizing-automatically
			if button_label:
				self.update_buttons(button.text(), button)
			else:
				self.update_buttons("color_"+colors[i], button)
			# print(button.text())

	@classmethod
	def update_buttons(cls, text: str, button):
		cls.buttons.update({text:button})




