import sys
import argparse
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow

from package.widgets.canvas import Canvas
from package.util.util import EnvSetting





if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Computer Graphics ToolKit")
	parser.add_argument("--env", required=True, help="Mandate, the environment used")

	args = parser.parse_args()
	env = args.env

	# System Setting
	EnvSetting.read_env_file("./env/" + env + ".env")
	
	# Initialize the Canvas
	canvas = Canvas()

	# Run
	sys.exit(canvas.app.exec())






