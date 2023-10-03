import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow

from package.widgets.canvas import Canvas
from package.widgets.toolkit import ToolKit
from package.util.util import EnvSetting





if __name__ == "__main__":

	# System Setting
	EnvSetting.read_env_file("./env/prd.env")
	
	# Initialize the Canvas
	canvas = Canvas()
	# Initialize the Tool Kit
	toolkit = ToolKit(canvas)
	toolkit.create_primitive_tools()

	# Run
	sys.exit(canvas.app.exec())






