import sys, math
from typing import List
from enum import Enum
from PyQt6 import QtCore
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout


from package.util import constant
from package.util.util import EnvSetting
from package.widgets.button import Buttons



class Layout(Enum):
	QHBoxLayout = QHBoxLayout()
	QVBoxLayout = QVBoxLayout()
	QGridLayout = QGridLayout()
	QFormLayout = QFormLayout()


def layout(l: str, widget_list):
		layout = Layout[l].value
		# layout.setSpacing(10)
		# layout.setContentsMargins(0, 0, 0, 0)
		# # Reference: https://stackoverflow.com/questions/67563632/how-to-reduce-the-space-between-two-widgets-in-pyqt5-qgridlayout#:~:text=To%20remove%20the%20space%20between,to%20the%20imaginary%20fifth%20column.

		if l == "QGridLayout":
			x = 0
			y = 0
			for widget in widget_list:
				if y >= int(EnvSetting.ENV[constant.NUMBER_OF_BUTTONS_IN_ROW]):
					x = x + 1
					y = 0
				layout.addWidget(widget_list[widget], x, y)
				y = y + 1
		elif l == "QFormLayout":
			for widget in range(len(widget_list)):
				layout.addRow(widget_list[widget][0], widget_list[widget][1])
		else:
			layout.addStretch(1)
			for widget in widget_list:
				layout.addWidget(widget_list[widget])

		return layout



def set_buttons_state(button_lable: str, enable = False):
	if enable:
		for button_text in Buttons.buttons:
			Buttons.buttons[button_text].setEnabled(True)
	else:
		for button_text in Buttons.buttons:
			# if not button_text == button_lable and not "color_#" in button_text:
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




def perform_transformation(matrix: List, vertex: List, ref_point: List = [0, 0]):
	#[ matrix[0][0] matrix[0][1] matrix[0][2] ][x]
	#[ matrix[1][0] matrix[1][1] matrix[1][2] ][y]
	#[ matrix[2][0] matrix[2][1] matrix[2][2] ][1]

	v = [\
			matrix[0][0]*(vertex[0] - ref_point[0]) + matrix[0][1]*(vertex[1] - ref_point[1]) + matrix[0][2]*vertex[2] + ref_point[0], \
			matrix[1][0]*(vertex[0] - ref_point[0]) + matrix[1][1]*(vertex[1] - ref_point[1]) + matrix[1][2]*vertex[2] + ref_point[1], \
			matrix[2][0]*(vertex[0] - ref_point[0]) + matrix[2][1]*(vertex[1] - ref_point[1]) + matrix[2][2]*vertex[2] ]

	return QPoint(v[0], v[1])




