from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QMessageBox, QPushButton, QLineEdit, QLabel


class Invalid_Input_Exception(Exception):
	def __init__(self, e):
		self.msgBox = QMessageBox()
		self.msgBox.setIcon(QMessageBox.Icon.Information)
		self.msgBox.setText("Invalid Input: No input received or invalid input range\n" + e)
		self.msgBox.setWindowTitle("Error")
		self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
		self.msgBox.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
		returnValue = self.msgBox.exec()


class No_Available_Graphics_Exception(Exception):
	def __init__(self, e):
		self.msgBox = QMessageBox()
		self.msgBox.setIcon(QMessageBox.Icon.Information)
		self.msgBox.setText("No available graphics\n" + e)
		self.msgBox.setWindowTitle("Error")
		self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
		self.msgBox.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
		returnValue = self.msgBox.exec()


class Transform_On_Vertex_Exception(Exception):
	def __init__(self):
		self.msgBox = QMessageBox()
		self.msgBox.setIcon(QMessageBox.Icon.Information)
		self.msgBox.setText("Unable to rotate or scale on: Vertex")
		self.msgBox.setWindowTitle("Error")
		self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
		self.msgBox.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
		returnValue = self.msgBox.exec()