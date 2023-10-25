from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QMessageBox, QPushButton, QLineEdit, QLabel


class General_Exception(Exception):
	def __init__(self):
		self.msgBox = QMessageBox()
		self.msgBox.setIcon(QMessageBox.Icon.Information)
		self.msgBox.setWindowTitle("Error")
		self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
		self.msgBox.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)


class Invalid_Input_Exception(General_Exception):
	def __init__(self, e):
		super(Invalid_Input_Exception, self).__init__()
		self.msgBox.setText("Invalid Input: No input received or invalid input range\n" + e)
		returnValue = self.msgBox.exec()


class No_Available_Graphics_Exception(General_Exception):
	def __init__(self, e):
		super(No_Available_Graphics_Exception, self).__init__()
		self.msgBox.setText("No available graphics\n" + e)
		returnValue = self.msgBox.exec()


class Transform_On_Vertex_Exception(General_Exception):
	def __init__(self):
		super(Transform_On_Vertex_Exception, self).__init__()
		self.msgBox.setText("Unable to rotate or scale on: Vertex")
		returnValue = self.msgBox.exec()