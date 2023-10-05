import sys
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