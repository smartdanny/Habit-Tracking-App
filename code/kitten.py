



import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QCoreApplication
from mouseTrack import mouseClickAndLocation
import time
import pandas as pd
import numpy as np
import math

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MouseLocPlot(MyMplCanvas):

    def compute_initial_figure(self):
        t = pd.read_csv('../data/mouseLoc.csv')['x']
        s = pd.read_csv('../data/mouseLoc.csv')['y']
        self.axes.plot(t, s)

class MouseClickPlot(MyMplCanvas):

    def compute_initial_figure(self):
        t = pd.read_csv('../data/mouseClicks.csv')['x']
        s = pd.read_csv('../data/mouseClicks.csv')['y']
        self.axes.plot(t, s)

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('kitten')
        self.setWindowIcon(QIcon('../images/kitten_16'))
        self.setGeometry(100, 100, 500, 400)
        self.home = Home(self)
        self.setCentralWidget(self.home)

        self.show()

class Home(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Set selections here
        self.mouse_movement_selection = False
        self.mouse_click_selection = False
        self.running_program_selection = False
        self.running_website_selection = False
        self.keyboard_input_selection = False

        # Threads to collect data
        self.mouse_clicks = None
        self.mouse_movement = None
        self.programs = None
        self.websites = None
        self.keyboard = None

        # initialize tab screen
        self.tabs = QTabWidget()
        self.home_tab = QWidget()
        self.data_select_tab = QWidget()
        self.mouse_movement_tab = QWidget()
        self.mouse_click_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.home_tab,"Home")
        self.tabs.addTab(self.data_select_tab,"Data Select")
        self.tabs.addTab(self.mouse_movement_tab, "Mouse Movements")
        self.tabs.addTab(self.mouse_click_tab, "Mouse Clicks")

        self.make_home_tab()
        self.make_data_select_tab()
        self.make_mouse_movement_tab()
        self.make_mouse_click_tab()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def make_home_tab(self):
        # Create welcome label
        kitten_lbl = QLabel(self)
        kitten_lbl.setText('Hi! Welcome to kitten :)')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(kitten_lbl)
        row_1.addStretch()

        # Add kitten image
        kitten_image_lbl = QLabel(self)
        kitten_image_lbl.setPixmap(QPixmap('../images/kitten_image.png'))
        row_2 = QHBoxLayout()
        row_2.addStretch()
        row_2.addWidget(kitten_image_lbl)
        row_2.addStretch()

    	# just another quit button for now
        data_select_btn = QPushButton('quit', self)
        data_select_btn.clicked.connect(QCoreApplication.instance().quit)
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(data_select_btn)
        row_3.addStretch()

        v_box = QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(row_1)
        v_box.addLayout(row_2)
        v_box.addLayout(row_3)
        v_box.addStretch(1) # This takes up space at the bottom.

        self.home_tab.setLayout(v_box)

    def make_data_select_tab(self):

        mouse_check_box = QCheckBox('mouse movements', self)
        mouse_check_box.stateChanged.connect(self.switch_mouse_movement_state)
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(mouse_check_box)
        row_1.addStretch()

        mouse_check_box = QCheckBox('mouse clicks', self)
        mouse_check_box.stateChanged.connect(self.switch_mouse_click_state)
        row_2 = QHBoxLayout()
        row_2.addStretch()
        row_2.addWidget(mouse_check_box)
        row_2.addStretch()

        mouse_check_box = QCheckBox('keyboard input', self)
        mouse_check_box.stateChanged.connect(self.switch_keyboard_input_state)
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(mouse_check_box)
        row_3.addStretch()

        mouse_check_box = QCheckBox('running programs', self)
        mouse_check_box.stateChanged.connect(self.switch_running_program_state)
        row_4 = QHBoxLayout()
        row_4.addStretch()
        row_4.addWidget(mouse_check_box)
        row_4.addStretch()

        mouse_check_box = QCheckBox('running websites', self)
        mouse_check_box.stateChanged.connect(self.switch_running_website_state)
        row_5 = QHBoxLayout()
        row_5.addStretch()
        row_5.addWidget(mouse_check_box)
        row_5.addStretch()

        data_select_btn = QPushButton('Begin Collecting Data!', self)
        data_select_btn.clicked.connect(self.initiate_data_collection)
        row_6 = QHBoxLayout()
        row_6.addStretch()
        row_6.addWidget(data_select_btn)
        row_6.addStretch()

        data_stop_btn = QPushButton('Stop Collecting Data!', self)
        data_stop_btn.clicked.connect(self.stop_data_collection)
        row_7 = QHBoxLayout()
        row_7.addStretch()
        row_7.addWidget(data_stop_btn)
        row_7.addStretch()

        v_box = QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(row_1)
        v_box.addLayout(row_2)
        v_box.addLayout(row_3)
        v_box.addLayout(row_4)
        v_box.addLayout(row_5)
        v_box.addLayout(row_6)
        v_box.addLayout(row_7)
        v_box.addStretch(1) # This takes up space at the bottom.

        self.data_select_tab.setLayout(v_box)

    def make_mouse_movement_tab(self):

        v_box = QVBoxLayout()

        lbl = QLabel(self)
        lbl.setText('Mouse Movements')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()

        vis_btn = QPushButton('Visualize Data', self)
        vis_btn.clicked.connect(lambda: self.plot_mouse_loc(row_2))
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(vis_btn)
        row_3.addStretch()

        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)

        self.mouse_movement_tab.setLayout(v_box)

    def make_mouse_click_tab(self):
        v_box = QVBoxLayout()

        lbl = QLabel(self)
        lbl.setText('Mouse Clicks')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()

        vis_btn = QPushButton('Visualize Data', self)
        vis_btn.clicked.connect(lambda: self.plot_mouse_clicks(row_2))
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(vis_btn)
        row_3.addStretch()

        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)

        self.mouse_click_tab.setLayout(v_box)

    def plot_mouse_loc(self, row):
        widget = MouseLocPlot(QWidget(self), width=5, height=4, dpi=100)
        row.addWidget(widget)
        row.addStretch()

    def plot_mouse_clicks(self, row):
        widget = MouseClickPlot(QWidget(self), width=5, height=4, dpi=100)
        row.addWidget(widget)
        row.addStretch()

    def initiate_data_collection(self):
        # Check for which boxes are ticked and start collecting data for those boxes
        if self.mouse_movement_selection and self.mouse_movement is None:
            self.record_mouse_movement()
        if self.mouse_click_selection and self.mouse_clicks is None:
            self.record_mouse_clicks()
        if self.running_program_selection and self.programs is None:
            self.record_running_programs()
        if self.running_website_selection and self.websites is None:
            self.record_running_websites()

    def stop_data_collection(self):
        if self.mouse_movement is not None:
            self.mouse_movement.recordLoc = False
            self.mouse_movement = None
        if self.mouse_clicks is not None:
            self.mouse_clicks.recordClicks = False
            self.mouse_clicks = None
        if self.programs is not None:
            self.programs = None
        if self.websites is not None:
            self.websites = None
        if self.keyboard is not None:
            self.keyboard = None

    def record_mouse_movement(self):
        # # initialize all event triggers to be clear (don't record anything)

        # create mouseListener thread
        self.mouse_movement = mouseClickAndLocation.MOUSETHREAD()
        self.mouse_movement.recordScroll = False
        self.mouse_movement.recordClicks = False
        self.mouse_movement.recordLoc = False
        self.mouse_movement.start()

        # turn on all event triggers
        self.mouse_movement.recordLoc = True

    def record_mouse_clicks(self):
        # # initialize all event triggers to be clear (don't record anything)

        # create mouseListener thread
        self.mouse_clicks = mouseClickAndLocation.MOUSETHREAD()
        self.mouse_clicks.recordScroll = False
        self.mouse_clicks.recordClicks = False
        self.mouse_clicks.recordLoc = False
        self.mouse_clicks.start()

        # turn on all event triggers
        self.mouse_clicks.recordClicks = True

    def record_running_programs(self):
        print('Recording running programs')

    def record_running_websites(self):
        print('Recording running websites')

    # Functions used to change the state of whether or not user wants data recorded #
    # Used in check boxes #
    def switch_mouse_movement_state(self):
        self.mouse_movement_selection = not self.mouse_movement_selection

    def switch_mouse_click_state(self):
        self.mouse_click_selection = not self.mouse_click_selection

    def switch_keyboard_input_state(self):
        self.keyboard_input_selection = not self.keyboard_input_selection

    def switch_running_program_state(self):
        self.running_program_selection = not self.running_program_selection

    def switch_running_website_state(self):
        self.running_website_selection = not self.running_website_selection



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
