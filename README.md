# Computer Graphics Toolkit

## Introduction
The Computer Graphics (CG) Toolkit is a program simulating off-the-shelf CG drawing software in terms of 2D graphics creation and manipulation. The simulation is accomplished by providing interactions through a user interface with built-in functions for creating objects, CG primitives, performing translation, rotation, scaling, and additional editing features. The goals include enhancing the understanding of fundamental operations and basic algorithms for computer graphics. The requirements are to develop a Computer Graphics Tool Kit by implementing the following computer graphics functions:
- [x] Creating objects with computer graphics primitives and their combinations
- [x] Object manipulation including translation, rotation, scaling and shearing
- [x] Object display with user interaction

<img width="1440" alt="Screenshot 2024-05-20 at 7 22 21 PM" src="https://github.com/BanjiBear/Computer-Graphic-ToolKit/assets/70761188/c5554f58-501c-499a-b4fe-49cc222284c4">
<img width="1191" alt="Screenshot 2024-05-20 at 7 24 55 PM" src="https://github.com/BanjiBear/Computer-Graphic-ToolKit/assets/70761188/8768a131-17a8-4909-bb5b-c76d9044126b">

## Environment
```
python 3.7.6 +
PyQt6
```
install PyQt6 with the following command:
```
pip install pyqt6
brew install pyqt
```
For Window users, an error may occur when installing the PyQt library through command prompt. The error should be something similar to:
```error: Microsoft Visual C++ 14.0 or greater is required. Get it with ......```
This is due to the fact that the PyQt library depends on C++ and the C++ compiler, and the machine is lacking such dependencies. To solve the problem, the solution is to navigate to the URL specified in the error message and download the visual C++. More information is described in [here](https://stackoverflow.com/questions/44951456/pip-error-microsoft-visual-c-14-0-is-required) and [here](https://wiki.python.org/moin/WindowsCompilers#Microsoft_Visual_C.2B-.2B-_14.0_standalone:_Visual_C.2B-.2B-_Build_Tools_2015_.28x86.2C_x64.2C_ARM.29). Once the visual C++ is installed, re-run the command again to install PyQt. 

## Program Execution
The system takes one parameter for running the Toolkit: the env file to be used. Users are able to create or customize the environmental variables in a .env file under the env folder. By default, a production env file named prd.env is created in advanced. Users can type in the following command to check for parameter details.
```
python3 -B main.py --help
```
To start the program/Toolkit, execute the following command
```
python3 -B main.py –env <env>
```

## Feature and Functionalities
For detailed description of all features with figure illustration, please refer to: [Section 2 of Application Report](https://github.com/BanjiBear/Computer-Graphic-ToolKit/blob/6916371797e9713bd7bad302cc117d3972a8f8b1/report/19084858d_CHENYIPU_ComputerGraphicsToolkitReport.pdf)
- Draw a Dot(vertex) on the canvas
- Draw a Line on the canvas
- Draw a Square on the canvas
- Draw a Rectangle on the canvas
- Draw a Circle on the canvas
- Draw a Triangle on the canvas
- Change colors of the objects
- Move, rotate, and scale the objects
- Undo the last action
- Redo the previous action

## Program Design and Architecture
The whole system solely implemented in Python leveraging the PyQt library. Cited online, PyQt is a Python binding for Qt, which is a set of C++ libraries and development tools providing platform-independent abstractions for graphical user interfaces (GUIs), allowing developers to create GUI applications. To put it simply, the PyQt library offer functions for GUI windows, buttons, texts, forms, input fields, painters, brushes, and so on. To ensure compatible with all devices, PyQt6 is chosen as it is still under continuous updates.

<img width="441" alt="Screenshot 2024-05-20 at 7 33 24 PM" src="https://github.com/BanjiBear/Computer-Graphic-ToolKit/assets/70761188/8266a641-266d-4915-a452-9eeef1df7319"><img width="481" alt="Screenshot 2024-05-20 at 8 22 01 PM" src="https://github.com/BanjiBear/Computer-Graphic-ToolKit/assets/70761188/cebedd80-5563-4521-8cb1-de5c8d179fe2">



The system architecture is ***devised in a way for easy modification and extension in the future.*** New features can be implemented easily by adding functions as behaviors of Classes. Secondly, as extending the program indicating more errors or exceptions to be handled. The system also granted capabilities to construct new exceptions with minimal effort. All exceptions inherit from a General_Exception, which defines the popup window, icon, titles, flags, and other basic settings. Users simply have to set custom error messages/texts and call the exec() to form new exceptions. Lastly, ***for both end users and developers, we extend the control of the system by isolating the window settings and environment configuration from the code into an env file. Not only users can be free from worries of altering the codes unconsciously, but developers can add new parameters and implement them independently.***


### Canvas Class
A canvas is created by the main function once executed. In order to create a GUI window, PyQt provides pre-defined ```QMainWindow``` and ```QWidgets``` Classes that can be inherit and overwritten. As specified in the official documentation, the ```QMainWindow``` is a framework for building application UI for main window management. Since the canvas will be the main window user perform drawings on, it is made to inherit the ```QMainWindow``` Class. The tools window is then imported and initialized within the canvas Class. The design guarantees that each canvas Class/window will be associated to one and only one tools window. Window configurations are done in the __init__ function. Configurations include window title, canvas color, and canvas size. The settings are stored in either constant or in the env file as parameters. If the size parameters are not set, the system detects the screen size and stretch the window to full screen.
```python
class Canvas(QMainWindow):

	def __init__(self):
		self.app = QApplication([])

		super().__init__()
		self.setWindowTitle(EnvSetting.ENV[constant.CANVAS_TITLE])
		self.setStyleSheet("background-color:" + constant.CANVAS_COLOR + ";")
		if int(EnvSetting.ENV[constant.CANVAS_WIDTH]) == 0 or int(EnvSetting.ENV[constant.CANVAS_HEIGHT]) == 0:
			screen = self.app.primaryScreen()
			self.setGeometry(0, 0, screen.size().width(), screen.size().height())
		else:
			self.setGeometry(0, 0, int(EnvSetting.ENV[constant.CANVAS_WIDTH]), int(EnvSetting.ENV[constant.CANVAS_HEIGHT]))
		self.show()

		# Initialize the Tool Kit
		self.toolkit = ToolKit()

```

### ToolKit Class
The toolkit Class is also a window with configurations set during initialization, the tools window is further set to always stay above the canvas through a flag. Since the canvas being the main window, the toolkit inherits the QWidgets Class only. An additional feature for both canvas and tools window are that the close button is disabled to prevent users from closing window before exiting the system.
```python
class ToolKit(QWidget):

	def __init__(self):
		parent = None
		super(ToolKit, self).__init__(parent)

		self.setWindowTitle(EnvSetting.ENV[constant.TOOLKIT_TITLE])
		self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
		self.toolkit_width, self.toolkit_height = int(EnvSetting.ENV[constant.TOOLKIT__WIDTH]), int(EnvSetting.ENV[constant.TOOLKIT__HEIGHT])

		self.buttons = Buttons(self.toolkit_width, self.toolkit_height)
		self.create_primitive_tools(self.buttons)
		self.create_color_palette(self.buttons)
		self.current_color = constant.DEFAULT_COLOR
		self.create_transformation_tools(self.buttons)
		self.create_other_tools(self.buttons)
		self.show()
```

### Buttons Class
Compared with the above two classes, the Buttons Class is rather simple. To generalize, the Class is only responsible for creating buttons (Button action and layout are defined in ToolKit Class and service packages). The buttons created are ```QPushButton``` from PyQt. Created buttons are stored in a Python dictionary, to prevent initializing Buttons object in different places, and to ensure consistence, a class method is created for updating and accessing buttons. This makes the created buttons associate with the Class instead of the instance.

### action_service and general_service
The action_service and general_service are service Classes. The action_service itself is a collection of Classes, including:
- Dot
- Line
- Quadrilateral
- Circle
- Triangle
- Actions, and
- Transformers

The primitives-related Classes store the graphics and set buttons status by calling functions in general_service. The Classes get event details from Canvas Class and configure the information into corresponding graphics/objects. Each Class holds a Dictionary (storage) and classmethods (updates) for easy access without the need to initialize any instance in anywhere while retaining consistency. The Actions Class also provides services for the undo and redo buttons. Two stacks are implemented to keep track of all user actions. These stacks are also associate with the Class, rather than the instance.
```python
class Actions:
	do = []
	redo = []



class Dot(QWidget):
	DOT: bool = False
	DOT_x, DOT_y = None,  None
	Dots: Dict = {}


class Line(QWidget):
	LINE: bool = False
	start_p, end_p = None, None
	Lines: Dict[int, Dict] = {}



class Quadrilateral(QWidget):
	QUAD: bool = False
	start_p, end_p = None, None
	mode: str = ""
	Rectangle: Dict[int, Dict] = {}
	Square: Dict[int, Dict] = {}



class Circle(QWidget):
	CIRCLE: bool = False
	central, circle_p = None, None
	Circles: Dict[int, Dict] = {}


class Triangle(QWidget):
	TRIANGEL: bool = False
	vertecies = []
	Triangles: Dict[int, Dict] = {}


class Transformer(QWidget):
    ...
```

### exception
As a GUI application, especially for CG drawings, the exceptions are design to show error messages in a popup window. Each exception in the exception package inherits the ```QWidgets``` Class to create a window of type ```QMessageBox```. The error messages are captured and embedded in pre-defined texts. The program is freeze-d until the confirmation button is clicked.
<img width="1112" alt="Screenshot 2024-05-20 at 8 00 43 PM" src="https://github.com/BanjiBear/Computer-Graphic-ToolKit/assets/70761188/f324dd6a-7a0d-449d-a4bb-d0aee7a8e79e">

### util and constant
The util package holds small snippets of functions that serve the system as a whole rather than specific functions or classes. Currently, it is used for Environmental Configurations. Constants are values or variables that remain unchanged under all condition and throughout the whole execution process. These values can be used globally once import the package.

