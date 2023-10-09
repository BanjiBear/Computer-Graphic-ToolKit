import sys, math
from PyQt6 import QtCore
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton

from package.widgets.button import Buttons



def set_buttons_state(button_lable: str, enable = False):
	if enable:
		for button_text in Buttons.buttons:
			Buttons.buttons[button_text].setEnabled(True)
	else:
		for button_text in Buttons.buttons:
			if not button_text == button_lable:
				Buttons.buttons[button_text].setEnabled(False)


def get_length(start_p: QPoint, end_p: QPoint):
	x_dev = start_p.x() - end_p.x()
	y_dev = start_p.y() - end_p.y()
	return math.sqrt((x_dev ** 2) + (y_dev ** 2))


def get_edge(start_p: QPoint, diagonal_p: QPoint):
	width = abs(start_p.x() - diagonal_p.x())
	height = abs(start_p.y() - diagonal_p.y())
	return width, height