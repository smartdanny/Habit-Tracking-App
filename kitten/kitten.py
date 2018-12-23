import sys
sys.path.append('./lib/')
import matplotlib
import os.path
import threading
import lib.mouseTrack.csvToDataFrameExample as csvHelper
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from os.path import expanduser
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,
                            QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QInputDialog,
                            QFileDialog, QMessageBox, QLineEdit, QDesktopWidget, QDialog, QTableWidget,
                            QTableWidget, QGridLayout, QGroupBox, QSpacerItem, QRadioButton, QButtonGroup, QShortcut,  QScrollArea)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QLinearGradient, QKeySequence
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt, QRect
import lib.mouseTrack.mouseClickAndLocation as mouseClickAndLocation
import lib.keyboardTrack.keyboardTracking as keyboardTracking
import lib.appTrack.appTracking as appScript
import lib.websiteTrack.proxyClient as proxyClient
import datetime
import time
import lib.mouseTrack.csvToDataFrameExample as csvImport
import pandas as pd
import numpy as np
import math
import string
import qtawesome as qta
import seaborn as sns
import lib.qrangeslider.qrangeslider as qrangeslider
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Globals
THEME = "Oranges_r" # default theme
keyboard_min_time_Stamp = 0
keyboard_max_time_Stamp = 0
mouse_min_time_Stamp = 0
mouse_max_time_Stamp = 0
app_min_time_Stamp = 0
app_max_time_Stamp = 0

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, type, min_time, max_time):
        self.screenSize = getScreenSize()
        global THEME
        global keyboard_min_time_Stamp
        global keyboard_max_time_Stamp
        global mouse_min_time_Stamp
        global mouse_max_time_Stamp
        keyboard_min_time_Stamp = 0
        keyboard_max_time_Stamp = 0
        mouse_min_time_Stamp = 0
        mouse_max_time_Stamp = 0
        if type == 'mouse':
            fig = self.compute_mouse(min_time, max_time)
        elif type == 'keyboard':
            fig = self.compute_keyboard(min_time, max_time)
        elif type == 'website':
            fig = self.compute_website(min_time, max_time)
        elif type == 'programs':
            fig = self.compute_programs(min_time, max_time)
        else: # default to mouse graph -- likely unnecessary
            fig = self.compute_mouse(min_time, max_time)
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def compute_mouse(self, min_time, max_time):
    	# NEED TO convert input min_time and max_time to values to compare with csv

        # clear figure before graphing
        plt.clf()
        global mouse_min_time_Stamp
        global mouse_max_time_Stamp

        # both exist
        if os.path.exists('./data/mouseLoc.csv') and os.path.exists('./data/mouseClicks.csv'):
            [loc, clicks, mouse_min_time_Stamp, mouse_max_time_Stamp] = getLocAndClicksDF(min_time, max_time)
            cbar_kws = { 'ticks' : [ 1,1 ] }
            sns.kdeplot(loc['x'], loc['y'], shade=True, cmap=THEME, cbar = True, cbar_kws = cbar_kws)
            plt.scatter(clicks['x'], clicks['y'], c="w", marker="+", label = 'clicks')

        else:
            if os.path.exists('./data/mouseLoc.csv'): # Just locations
                [loc, mouse_min_time_Stamp, mouse_max_time_Stamp] = getLocDF(min_time, max_time)
                sns.kdeplot(loc['x'], loc['y'], shade=True, cmap=THEME, cbar = True)

            else: # Just Clicks
                [clicks, mouse_min_time_Stamp, mouse_max_time_Stamp] = getClicksDF(min_time, max_time)
                plt.scatter(clicks['x'], clicks['y'], c="w", marker="+", label = 'clicks')

        # Set X and Y limits
        plt.ylim(0, self.screenSize.height()) #limits minimum and maximum values on graph to fit screen size
        plt.xlim(0, self.screenSize.width()) #limits minimum and maximum values on graph to fit screen size

        # Flip y axis and change label location
        ax = plt.gca()
        ax.set_ylim(ax.get_ylim()[::-1])
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')


        plt.legend()
        # get current pyplot figure
        g = plt.gcf()
        print('\nClick range from ' + str(mouse_min_time_Stamp) + ' to ' + str(mouse_max_time_Stamp))
        return g

    def compute_keyboard(self, min_time, max_time):
        global keyboard_min_time_Stamp
        global keyboard_max_time_Stamp
        [keys, keyboard_min_time_Stamp, keyboard_max_time_Stamp] = getKeysDF(min_time, max_time)

        # translate keys to image coordinates
        d= []
        for k in keys['Key']:
            if "backspace" in k:      # SPECIAL KEYS
                d.append((670,25))
            elif "space" in k:
            	d.append((325,225))
            elif "tab" in k:
            	d.append((35,75))
            elif "caps_lock" in k:
            	d.append((40,125))
            elif "menu" in k:
            	d.append((620,225))
            elif "ctrl_l" in k:       # default all left/right keys to right
            	d.append((40,225))
            elif "ctrl" in k:
            	d.append((685,225))
            elif "shift_l" in k:
            	d.append((55,175))
            elif "shift" in k:
            	d.append((655,175))
            elif "alt_l" in k:
            	d.append((162,225))
            elif "alt" in k:
            	d.append((500,225))
            elif "cmd_l" in k:
            	d.append((100,225))
            elif "cmd" in k:
            	d.append((560,225))
            elif "a" in k:            # ALPHABET
                d.append((110,125))
            elif "b" in k:
                d.append((330,175))
            elif "c" in k:
                d.append((230, 175))
            elif "d" in k:
                d.append((205,125))
            elif "e" in k:
                d.append((195,75))
            elif "f" in k:
                d.append((255, 125))
            elif "g" in k:
                d.append((303,125))
            elif "h" in k:
                d.append((353,125))
            elif "i" in k:
                d.append((435, 75))
            elif "j" in k:
                d.append((400,125))
            elif "k" in k:
                d.append((450,125))
            elif "l" in k:
                d.append((500,125))
            elif "m" in k:
                d.append((425,175))
            elif "n" in k:
                d.append((375,175))
            elif "o" in k:
                d.append((485,75))
            elif "p" in k:
                d.append((530,75))
            elif "q" in k:
                d.append((100,75))
            elif "r" in k:
                d.append((245,75))
            elif "s" in k:
                d.append((160,125))
            elif "t" in k:
                d.append((290,75))
            elif "u" in k:
                d.append((390,75))
            elif "v" in k:
                d.append((280,75))
            elif "w" in k:
                d.append((148,75))
            elif "x" in k:
                d.append((180,175))
            elif "y" in k:
                d.append((340,75))
            elif "z" in k:
                d.append((130,175))
            elif "~" in k or "`" in k: # SYMBOLS & NUMBERS
                d.append((25,25))
            elif "1" in k or "!" in k:
                d.append((75,25))
            elif "2" in k or "@" in k:
                d.append((125,25))
            elif "3" in k or "#" in k:
                d.append((170,25))
            elif "4" in k or "$" in k:
                d.append((218,25))
            elif "5" in k or "%" in k:
                d.append((265,25))
            elif "6" in k or "^" in k:
            	d.append((315, 25))
            elif "7" in k or "&" in k:
            	d.append((362,25))
            elif "8" in k or "*" in k:
            	d.append((410,25))
            elif "9" in k or "(" in k:
            	d.append((460,25))
            elif "0" in k or ")" in k:
            	d.append((505,25))
            elif "-" in k or "_" in k:
            	d.append((555,25))
            elif "+" in k or "=" in k:
            	d.append((600,25))
            elif "{" in k or "[" in k:
            	d.append((580,75))
            elif "{" in k or "]" in k:
            	d.append((625,75))
            elif "\\" in k or "|" in k:
            	d.append((685,75))
            elif ":" in k or ";" in k:
            	d.append((545,125))
            elif "'" in k or '"' in k:
            	d.append((590,125))
            elif "<" in k or "comma" in k:
            	d.append((470,175))
            elif ">" in k or "." in k:
            	d.append((515,175))
            elif "?" in k or "/" in k:
            	d.append((565,175))
            else:
                pass  # ignore buttons not on standard keyboard


        df = pd.DataFrame(data=d, columns=['x','y'], dtype=int)
        # clear figure before graphing
        plt.clf()
        # graph onto figure
        sns.kdeplot(df.x, df.y, shade=True, shade_lowest=False, cmap=THEME, alpha=0.6)
        keyboard = mpimg.imread('./images/keyboard.png')
        plt.imshow(keyboard)
        g = plt.gcf() # get current figure

        print('\nKeyboard range from ' + str(keyboard_min_time_Stamp) + ' to ' + str(keyboard_max_time_Stamp))
        return g

    def compute_website(self, min_time = 0, max_time = 0):
        # websites = pd.read_csv('./data/websites.csv')
        # example data, real data read in from csv
        websites = 'Facebook', 'Reddit', 'Canvas', 'GitHub',
        times = [12,11,3,30]

        # clear figure before graphing
        plt.clf()
        # graph onto figure
        if (THEME == "plasma"):
            cmap=matplotlib.cm.plasma(np.arange(0,1,.15))
        elif (THEME=="viridis"):
        	cmap=matplotlib.cm.viridis(np.arange(0,1,.15))
        elif (THEME=="magma"):
        	cmap=matplotlib.cm.magma(np.arange(0,1,.15))
        elif (THEME=="inferno"):
        	cmap=matplotlib.cm.inferno(np.arange(0,1,.15))
        elif (THEME=="Reds_r"):
        	cmap=matplotlib.cm.Reds(np.arange(0.2,1,.1))
        elif (THEME=="Purples_r"):
        	cmap=matplotlib.cm.Purples(np.arange(0.2,1,.1))
        elif (THEME=="Blues_r"):
        	cmap=matplotlib.cm.Blues(np.arange(0.2,1,.1))
        elif (THEME=="Greens_r"):
        	cmap=matplotlib.cm.Greens(np.arange(0.2,1,.1))
        elif (THEME=="Greys_r"):
        	cmap=matplotlib.cm.Greys(np.arange(0.2,1,.1))
        else:
            cmap=matplotlib.cm.Oranges(np.arange(0.2,1,.1))
        my_circle = plt.Circle( (0,0), 0.7, color='white')
        plt.pie(times, labels=websites, colors=cmap)
        g = plt.gcf() # get current figure
        g.gca().add_artist(my_circle)
        return g

    def compute_programs(self, min_time, max_time):
        global app_min_time_Stamp
        global app_max_time_Stamp
        [apps, app_min_time_Stamp, app_max_time_Stamp] = getAppDF(min_time, max_time)

        print("GRAPHING APP INFORMATION///////////////// \n")
        print(apps['App'].value_counts())

        # appsGraphInfo = np.array(apps['App'].value_counts())
        appsGraphInfo = list(apps['App'].value_counts())
        appsGraphIndex = list(apps['App'].value_counts().index)
        print(appsGraphInfo)
        print(appsGraphIndex)
        print('\n\n\n')
        # print(appsGraphInfo.iloc['App'])

        # clear figure before graphing
        plt.clf()
        # graph onto figure
        if (THEME == "plasma"):
            cmap=matplotlib.cm.plasma(np.arange(0,1,.15))
        elif (THEME=="viridis"):
        	cmap=matplotlib.cm.viridis(np.arange(0,1,.15))
        elif (THEME=="magma"):
        	cmap=matplotlib.cm.magma(np.arange(0,1,.15))
        elif (THEME=="inferno"):
        	cmap=matplotlib.cm.inferno(np.arange(0,1,.15))
        elif (THEME=="Reds_r"):
        	cmap=matplotlib.cm.Reds(np.arange(0.2,1,.1))
        elif (THEME=="Purples_r"):
        	cmap=matplotlib.cm.Purples(np.arange(0.2,1,.1))
        elif (THEME=="Blues_r"):
        	cmap=matplotlib.cm.Blues(np.arange(0.2,1,.1))
        elif (THEME=="Greens_r"):
        	cmap=matplotlib.cm.Greens(np.arange(0.2,1,.1))
        elif (THEME=="Greys_r"):
        	cmap=matplotlib.cm.Greys(np.arange(0.2,1,.1))
        else:
            cmap=matplotlib.cm.Oranges(np.arange(0.2,1,.1))

        my_circle=plt.Circle( (0,0), 0.7, color='white')
        plt.pie(x=appsGraphInfo, labels=appsGraphIndex, colors=cmap)
        g = plt.gcf() # get current figure
        g.gca().add_artist(my_circle) # adds white circle to Artist -- parent of g
        return g

class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()

        # Set title, icon, and size
        self.setWindowIcon(QIcon('./images/logo-256x256'))
        self.setWindowTitle("About")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(625, 250)

        # Create About text
        about_text = QLabel('''
        Kitten is a general habit-tracking application with a multitude of
        modularized tracking features including recording mouse movement,
        key presses, time spent on computer applications, and time spent on
        websites. Kitten's functionality was created to support and benefit
        gamers, teachers, parents, the typical Internet and computer
        user, and more.
        ''')
        about_text.setAlignment(Qt.AlignCenter)

        # Create first row
        about_row_1 = QHBoxLayout()
        about_row_1.addStretch()
        about_row_1.addWidget(about_text)
        about_row_1.addStretch()

        # Create OK button
        about_ok_btn = QPushButton("OK")
        about_ok_btn.clicked.connect(self.close)

        # Create second row
        about_row_2 = QHBoxLayout()
        about_row_2.addStretch()
        about_row_2.addWidget(about_ok_btn)
        about_row_2.addStretch()

        # Vertical layout
        about_v_box = QVBoxLayout()
        about_v_box.addLayout(about_row_1)
        about_v_box.addStretch(1)
        about_v_box.addLayout(about_row_2)
        about_v_box.addStretch(1)
        self.setLayout(about_v_box)

        self.setStyleSheet('''
        QLabel, QPushButton {
            font: 11pt Myriad Pro;
            color: black;
        }
        ''')

class CustomizeDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Set title, icon, and size
        self.setWindowIcon(QIcon('./images/logo-256x256'))
        self.setWindowTitle("Customize")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(625, 250)

        self.tabs = QTabWidget()
        self.themes_tab = QWidget()

        self.tabs.addTab(self.themes_tab, qta.icon('fa.paint-brush'), "Themes")

        self.make_themes_tab()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.setStyleSheet('''
        QLabel, QPushButton {
            font: 11pt Myriad Pro;
            color: black;
        }
        ''')

    def make_themes_tab(self):

        # Create About text
        theme_lbl = QLabel('Themes')
        theme_lbl.setAlignment(Qt.AlignCenter)

        # Create first row
        themes_row_1 = QHBoxLayout()
        themes_row_1.addStretch()
        themes_row_1.addWidget(theme_lbl)
        themes_row_1.addStretch()

        # List of themes
        self.plasma_theme_btn = QRadioButton("Plasma")
        plasma_theme_lbl = QLabel(self)
        plasma_theme_lbl.setPixmap(QPixmap('./images/plasma.png'))
        plasma_theme_row = QHBoxLayout()
        plasma_theme_row.addWidget(self.plasma_theme_btn)
        plasma_theme_row.addWidget(plasma_theme_lbl)

        self.viridis_theme_btn = QRadioButton("Viridis")
        viridis_theme_lbl = QLabel(self)
        viridis_theme_lbl.setPixmap(QPixmap('./images/viridis.png'))
        viridis_theme_row = QHBoxLayout()
        viridis_theme_row.addWidget(self.viridis_theme_btn)
        viridis_theme_row.addWidget(viridis_theme_lbl)

        self.magma_theme_btn = QRadioButton("Magma")
        magma_theme_lbl = QLabel(self)
        magma_theme_lbl.setPixmap(QPixmap('./images/magma.png'))
        magma_theme_row = QHBoxLayout()
        magma_theme_row.addWidget(self.magma_theme_btn)
        magma_theme_row.addWidget(magma_theme_lbl)

        self.inferno_theme_btn = QRadioButton("Inferno")
        inferno_theme_lbl = QLabel(self)
        inferno_theme_lbl.setPixmap(QPixmap('./images/inferno.png'))
        inferno_theme_row = QHBoxLayout()
        inferno_theme_row.addWidget(self.inferno_theme_btn)
        inferno_theme_row.addWidget(inferno_theme_lbl)

        self.oranges_theme_btn = QRadioButton("Oranges")
        self.oranges_theme_btn.setChecked(True)
        oranges_theme_lbl = QLabel(self)
        oranges_theme_lbl.setPixmap(QPixmap('./images/oranges.png'))
        oranges_theme_row = QHBoxLayout()
        oranges_theme_row.addWidget(self.oranges_theme_btn)
        oranges_theme_row.addWidget(oranges_theme_lbl)

        self.reds_theme_btn = QRadioButton("Reds")
        reds_theme_lbl = QLabel(self)
        reds_theme_lbl.setPixmap(QPixmap('./images/reds.png'))
        reds_theme_row = QHBoxLayout()
        reds_theme_row.addWidget(self.reds_theme_btn)
        reds_theme_row.addWidget(reds_theme_lbl)

        self.purples_theme_btn = QRadioButton("Purples")
        purples_theme_lbl = QLabel(self)
        purples_theme_lbl.setPixmap(QPixmap('./images/purples.png'))
        purples_theme_row = QHBoxLayout()
        purples_theme_row.addWidget(self.purples_theme_btn)
        purples_theme_row.addWidget(purples_theme_lbl)

        self.blues_theme_btn = QRadioButton("Blues")
        blues_theme_lbl = QLabel(self)
        blues_theme_lbl.setPixmap(QPixmap('./images/blues.png'))
        blues_theme_row = QHBoxLayout()
        blues_theme_row.addWidget(self.blues_theme_btn)
        blues_theme_row.addWidget(blues_theme_lbl)

        self.greens_theme_btn = QRadioButton("Greens")
        greens_theme_lbl = QLabel(self)
        greens_theme_lbl.setPixmap(QPixmap('./images/greens.png'))
        greens_theme_row = QHBoxLayout()
        greens_theme_row.addWidget(self.greens_theme_btn)
        greens_theme_row.addWidget(greens_theme_lbl)

        self.greys_theme_btn = QRadioButton("Greys")
        greys_theme_lbl = QLabel(self)
        greys_theme_lbl.setPixmap(QPixmap('./images/greys.png'))
        greys_theme_row = QHBoxLayout()
        greys_theme_row.addWidget(self.greys_theme_btn)
        greys_theme_row.addWidget(greys_theme_lbl)

        # Create OK button
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.close)

        # Create Apply button
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(lambda: self.choose_theme())

        # Create second row
        themes_row_2 = QHBoxLayout()
        themes_row_2.addStretch()
        themes_row_2.addWidget(ok_btn)
        themes_row_2.addWidget(apply_btn)
        themes_row_2.addStretch()

        # Vertical layout
        themes_v_box = QVBoxLayout()
        themes_v_box.addLayout(themes_row_1)
        themes_v_box.addLayout(plasma_theme_row)
        themes_v_box.addLayout(viridis_theme_row)
        themes_v_box.addLayout(magma_theme_row)
        themes_v_box.addLayout(inferno_theme_row)
        themes_v_box.addLayout(oranges_theme_row)
        themes_v_box.addLayout(reds_theme_row)
        themes_v_box.addLayout(purples_theme_row)
        themes_v_box.addLayout(blues_theme_row)
        themes_v_box.addLayout(greens_theme_row)
        themes_v_box.addLayout(greys_theme_row)
        themes_v_box.addLayout(themes_row_2)
        themes_v_box.addStretch(1)

        self.themes_tab.setLayout(themes_v_box)

    def choose_theme(self):
        global THEME
        if self.plasma_theme_btn.isChecked():
            THEME='plasma'
        elif self.viridis_theme_btn.isChecked():
            THEME='viridis'
        elif self.magma_theme_btn.isChecked():
            THEME='magma'
        elif self.inferno_theme_btn.isChecked():
            THEME='inferno'
        elif self.oranges_theme_btn.isChecked():
            THEME='Oranges_r'
        elif self.reds_theme_btn.isChecked():
            THEME='Reds_r'
        elif self.purples_theme_btn.isChecked():
            THEME='Purples_r'
        elif self.blues_theme_btn.isChecked():
            THEME='Blues_r'
        elif self.greens_theme_btn.isChecked():
            THEME='Greens_r'
        elif self.greys_theme_btn.isChecked():
            THEME='Greys_r'
        # REFRESH PICS

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set title
        self.setWindowTitle('Kitten')

        # Set logo icon
        self.setWindowIcon(QIcon('./images/logo-256x256'))

        # Resize and center the window
        self.resize(925, 600);
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Create stylsheet
        self.setStyleSheet('''
        QLabel#subtitle {
            font: bold "Myriad Pro";
            font-size: 30px;
            color: #E5943C;
        }
        QLabel, QPushButton {
            font: 11pt Myriad Pro;
            color: black;
        }
        QLabel#tab_title {
            font: 30px;
        }
        QLabel#sub-help {
            font: bold 22px;
            padding-bottom: 30px;
        }
        QLabel#help {
            font: italic 22px;
        }
        QTabBar::tab {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                    stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        border: 1px solid #C4C4C3;
        border-bottom-color: #C2C7CB; /* same as the pane color */
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 8ex;
        padding: 2px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                    stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }
        QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: #C2C7CB; /* same as pane color */
        }
        QTabBar::tab:!selected {
            margin-top: 2px; /* make non-selected tabs look smaller */
        }
        QPushButton {

        }
        ''')

        # Show the window
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
        self.apps = None
        self.websites = None
        self.keyboard = None

        # local variables to check when data is to be collected
        self.websites_to_record = []
        self.programs_to_record = []

        # initialize tab screen
        self.tabs = QTabWidget()
        self.home_tab = QWidget()
        self.data_select_tab = QWidget()
        self.mouse_tab = QWidget()
        self.mouse_click_tab = QWidget()
        self.keyboard_tab = QWidget()
        self.websites_tab = QWidget()
        self.programs_tab = QWidget()
        self.help_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.home_tab, qta.icon('fa.home'),"Home")
        self.tabs.addTab(self.data_select_tab, qta.icon('fa.list'), "Data Select")
        self.tabs.addTab(self.mouse_tab, qta.icon('fa.mouse-pointer'),"Mouse")
        self.tabs.addTab(self.keyboard_tab, qta.icon('fa.th'),"Keyboard")
        self.tabs.addTab(self.websites_tab, qta.icon('fa.globe'),"Websites")
        self.tabs.addTab(self.programs_tab, qta.icon('fa.desktop'),"Programs")
        self.tabs.addTab(self.help_tab, qta.icon('fa.question-circle'),"Help")

        self.make_home_tab()
        self.make_data_select_tab()
        self.make_mouse_tab()
        self.make_keyboard_tab()
        self.make_websites_tab()
        self.make_programs_tab()
        self.make_help_tab()

        # Keyboard shortcuts
        self.home_shortcut = QShortcut(QKeySequence("Ctrl+1"), self)
        self.home_shortcut.activated.connect(self.open_home)
        self.data_select_shortcut = QShortcut(QKeySequence("Ctrl+2"), self)
        self.data_select_shortcut.activated.connect(self.open_data_select)
        self.mouse_shortcut = QShortcut(QKeySequence("Ctrl+3"), self)
        self.mouse_shortcut.activated.connect(self.open_mouse)
        self.keyboard_shortcut = QShortcut(QKeySequence("Ctrl+4"), self)
        self.keyboard_shortcut.activated.connect(self.open_keyboard)
        self.websites_shortcut = QShortcut(QKeySequence("Ctrl+5"), self)
        self.websites_shortcut.activated.connect(self.open_websites)
        self.programs_shortcut = QShortcut(QKeySequence("Ctrl+6"), self)
        self.programs_shortcut.activated.connect(self.open_programs)
        self.help_shortcut = QShortcut(QKeySequence("Ctrl+7"), self)
        self.help_shortcut.activated.connect(self.open_help)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def open_home(self):
        self.tabs.setCurrentWidget(self.home_tab)
    def open_data_select(self):
        self.tabs.setCurrentWidget(self.data_select_tab)
    def open_mouse(self):
        self.tabs.setCurrentWidget(self.mouse_tab)
    def open_keyboard(self):
        self.tabs.setCurrentWidget(self.keyboard_tab)
    def open_websites(self):
        self.tabs.setCurrentWidget(self.websites_tab)
    def open_programs(self):
        self.tabs.setCurrentWidget(self.programs_tab)
    def open_help(self):
        self.tabs.setCurrentWidget(self.help_tab)

    def make_home_tab(self):

        # Add top border
        border_top = QLabel(self)
        border_top.setPixmap(QPixmap('./images/' + THEME + '_top.png'))
        row_0 = QHBoxLayout()
        row_0.addWidget(border_top)

        # Add kitten image
        kitten_image_lbl = QLabel(self)
        kitten_image_lbl.setPixmap(QPixmap('./images/full-logo-375x135'))
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(kitten_image_lbl)
        row_1.addStretch()

        # Add about text
        about_text = QLabel('A Habit Tracking Application')
        about_text.setAlignment(Qt.AlignCenter)
        about_text.setObjectName("subtitle")
        row_2 = QHBoxLayout()
        row_2.addStretch()
        row_2.addWidget(about_text)
        row_2.addStretch()

    	# Just another quit button for now
        quit_btn = QPushButton('Quit', self)
        quit_btn.clicked.connect(QCoreApplication.instance().quit)

        # About button and dialog modal
        about_btn = QPushButton('About', self)
        about_dialog = AboutDialog()
        about_btn.clicked.connect(lambda: about_dialog.exec_())

        # Customize Home button
        customize_btn = QPushButton(qta.icon('fa.cog'), 'Customize', self)
        customize_dialog = CustomizeDialog()
        customize_btn.clicked.connect(lambda: customize_dialog.exec_())

        # Row 3 buttons
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(customize_btn)
        row_3.addWidget(about_btn)
        row_3.addWidget(quit_btn)
        row_3.addStretch()

        # add version number at the bottom of the GUI
        version_number = QLabel("1.0.0")
        version_number.setAlignment(Qt.AlignRight)
        row_4 = QHBoxLayout()
        row_4.addWidget(version_number)

        # Add bottom border
        border_bottom = QLabel(self)
        border_bottom.setPixmap(QPixmap('./images/' + THEME + '_bottom.png'))
        row_5 = QHBoxLayout()
        row_5.addWidget(border_bottom)

        v_box = QVBoxLayout()
        v_box.addLayout(row_0)
        v_box.addStretch(1)
        v_box.addLayout(row_1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)
        v_box.addLayout(row_4)
        v_box.addLayout(row_5)

        self.home_tab.setLayout(v_box)

    def make_data_select_tab(self):

        # Add top border
        border_top = QLabel(self)
        border_top.setPixmap(QPixmap('./images/' + THEME + '_top.png'))
        border_top_row = QHBoxLayout()
        border_top_row.addWidget(border_top)

        data_select_title = QLabel('Data Select')
        data_select_title.setObjectName('tab_title')
        row_0 = QHBoxLayout()
        row_0.addStretch()
        row_0.addWidget(data_select_title)
        row_0.addStretch()

        data_layout = QGridLayout()
        data_layout.setColumnStretch(0, 4)
        data_layout.setColumnStretch(2, 7)

        mouse_lbl = QLabel('Mouse')
        mouse_movements_check_box = QCheckBox('Movement', self)
        mouse_movements_check_box.stateChanged.connect(self.switch_mouse_movement_state)
        mouse_clicks_check_box = QCheckBox('Clicks', self)
        mouse_clicks_check_box.stateChanged.connect(self.switch_mouse_click_state)
        data_layout.addWidget(mouse_lbl, 1, 1)
        data_layout.addWidget(mouse_movements_check_box, 2, 1)
        data_layout.addWidget(mouse_clicks_check_box, 2, 2)
        data_layout.addWidget(QLabel(''), 3, 1)

        keyboard_lbl = QLabel('Keyboard')
        keyboard_check_box = QCheckBox('Keyboard Input', self)
        keyboard_check_box.stateChanged.connect(self.switch_keyboard_input_state)
        data_layout.addWidget(keyboard_lbl, 4, 1)
        data_layout.addWidget(keyboard_check_box, 5, 1)
        data_layout.addWidget(QLabel(' '), 6, 1)

        programs_lbl = QLabel('Programs')
        programs_check_box = QCheckBox('Programs', self)
        self.programs_le = QLineEdit()
        self.programs_le.setPlaceholderText('Ex: \'slack,photoshop \' ')
        self.programs_le.setEnabled(False)
        programs_check_box.stateChanged.connect(self.switch_running_program_state)
        data_layout.addWidget(programs_lbl, 7, 1)
        data_layout.addWidget(programs_check_box, 8, 1)
        data_layout.addWidget(self.programs_le, 8, 2)
        data_layout.addWidget(QLabel(' '), 9, 1)

        websites_lbl = QLabel('Websites')
        websites_check_box = QCheckBox('Websites', self)
        self.websites_le = QLineEdit()
        self.websites_le.setFixedWidth(300)
        self.websites_le.setPlaceholderText('Ex: facebook.com, twitter.com')
        self.websites_le.setEnabled(False)
        websites_check_box.stateChanged.connect(self.switch_running_website_state)
        data_layout.addWidget(websites_lbl, 10, 1)
        data_layout.addWidget(websites_check_box, 11, 1)
        data_layout.addWidget(self.websites_le, 11, 2)
        data_layout.addWidget(QLabel(' '), 12, 1)

        data_stop_btn = QPushButton(qta.icon('fa.stop', color='red'), 'Stop Collecting Data!', self)
        data_stop_btn.setEnabled(False)
        data_select_btn = QPushButton(qta.icon('fa.play',color='green'), 'Begin Collecting Data!', self)
        data_select_btn.clicked.connect(lambda: self.initiate_data_collection(self.websites_le, self.programs_le, data_stop_btn, data_select_btn))
        data_stop_btn.clicked.connect(lambda: self.stop_data_collection(data_stop_btn, data_select_btn))
        row_6 = QHBoxLayout()
        row_6.addStretch()
        row_6.addWidget(data_select_btn)
        row_6.addWidget(data_stop_btn)
        row_6.addStretch()

        # Add bottom border
        border_bottom = QLabel(self)
        border_bottom.setPixmap(QPixmap('./images/' + THEME + '_bottom.png'))
        border_bottom_row = QHBoxLayout()
        border_bottom_row.addWidget(border_bottom)

        v_box = QVBoxLayout()
        v_box.addLayout(border_top_row)
        v_box.addLayout(row_0)
        v_box.addStretch(1)
        v_box.addLayout(data_layout)
        v_box.addStretch(1)
        v_box.addLayout(row_6)
        v_box.addStretch(1) # This takes up space at the bottom.
        v_box.addLayout(border_bottom_row)

        self.data_select_tab.setLayout(v_box)

    def timeInputDialog(self):
        month_le = QLineEdit()
        month_le.setPlaceholderText('Month')
        day_le = QLineEdit()
        day_le.setPlaceholderText('Day')
        year_le = QLineEdit()
        year_le.setPlaceholderText('Year')
        hour_le = QLineEdit()
        hour_le.setPlaceholderText('Hour')
        min_le = QLineEdit()
        min_le.setPlaceholderText('Minute')
        sec_le = QLineEdit()
        sec_le.setPlaceholderText('Second')
        AMorPM_le = QLineEdit()
        AMorPM_le.setPlaceholderText('AM/PM')
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(month_le)
        row.addWidget(day_le)
        row.addWidget(year_le)
        row.addWidget(hour_le)
        row.addWidget(min_le)
        row.addWidget(sec_le)
        row.addWidget(AMorPM_le)
        return row

    def make_mouse_tab(self):

        v_box = QVBoxLayout()

        # Add top border
        border_top = QLabel(self)
        border_top.setPixmap(QPixmap('./images/' + THEME + '_top.png'))
        border_top_row = QHBoxLayout()
        border_top_row.addWidget(border_top)

        mouse_lbl = QLabel('Mouse', self)
        mouse_lbl.setObjectName('tab_title')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(mouse_lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()
        vis_btn = QPushButton(qta.icon('fa.pie-chart',color='orange'),'Visualize Data', self)
        download_btn = QPushButton(qta.icon('fa.download', color='green'),'Download Data', self)
        range_slider = qrangeslider.QRangeSlider()


        # row_3 = QHBoxLayout()
        # row_3.addStretch()


        # range_slider.startValueChanged.connect(lambda: self.plot_mouse_loc(row_2, range_slider.start(), range_slider.end()))
        # range_slider.endValueChanged.connect(lambda: self.plot_mouse_loc(row_2, range_slider.start(), range_slider.end()))
        vis_btn.clicked.connect(lambda: self.plot_mouse_loc(row_2, range_slider.start(), range_slider.end()))
        download_btn.clicked.connect(lambda: self.download_data('mouseLoc.csv', range_slider.start(), range_slider.end()))



        row_5 = QHBoxLayout()
        row_5.addStretch()
        row_5.addWidget(vis_btn)
        row_5.addWidget(download_btn)
        row_5.addWidget(range_slider)
        row_5.addStretch()

        # Add bottom border
        border_bottom = QLabel(self)
        border_bottom.setPixmap(QPixmap('./images/' + THEME + '_bottom.png'))
        border_bottom_row = QHBoxLayout()
        border_bottom_row.addWidget(border_bottom)

        v_box.addLayout(border_top_row)
        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        # v_box.addLayout(row_3)
        # v_box.addStretch(1)
        v_box.addLayout(row_5)
        v_box.addLayout(border_bottom_row)

        self.mouse_tab.setLayout(v_box)

    def make_keyboard_tab(self):

        # Add top border
        border_top = QLabel(self)
        border_top.setPixmap(QPixmap('./images/' + THEME + '_top.png'))
        border_top_row = QHBoxLayout()
        border_top_row.addWidget(border_top)

        v_box = QVBoxLayout()

        keyboard_lbl = QLabel('Keyboard', self)
        keyboard_lbl.setObjectName('tab_title')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(keyboard_lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()

        vis_btn = QPushButton(qta.icon('fa.pie-chart',color='orange'),'Visualize Data', self)
        download_btn = QPushButton(qta.icon('fa.download', color='green'),'Download Data', self)
        range_slider = qrangeslider.QRangeSlider()
        vis_btn.clicked.connect(lambda: self.plot_keyboard_input(row_2, range_slider.start(), range_slider.end()))
        download_btn.clicked.connect(lambda: self.download_data('keyboard.csv', range_slider.start(), range_slider.end()))
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(vis_btn)
        row_3.addWidget(download_btn)
        row_3.addWidget(range_slider)
        row_3.addStretch()

        # Add bottom border
        border_bottom = QLabel(self)
        border_bottom.setPixmap(QPixmap('./images/' + THEME + '_bottom.png'))
        border_bottom_row = QHBoxLayout()
        border_bottom_row.addWidget(border_bottom)

        v_box.addLayout(border_top_row)
        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)
        v_box.addLayout(border_bottom_row)

        self.keyboard_tab.setLayout(v_box)

    def make_websites_tab(self):
        v_box = QVBoxLayout()

        # Add top border
        border_top = QLabel(self)
        border_top.setPixmap(QPixmap('./images/' + THEME + '_top.png'))
        border_top_row = QHBoxLayout()
        border_top_row.addWidget(border_top)

        websites_lbl = QLabel('Websites', self)
        websites_lbl.setObjectName('tab_title')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(websites_lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()

        vis_btn = QPushButton(qta.icon('fa.pie-chart',color='orange'),'Visualize Data', self)
        download_btn = QPushButton(qta.icon('fa.download', color='green'),'Download Data', self)
        range_slider = qrangeslider.QRangeSlider()
        vis_btn.clicked.connect(lambda: self.plot_website(row_2, range_slider.start(), range_slider.end()))
        download_btn.clicked.connect(lambda: self.download_data('websites.csv', range_slider.start(), range_slider.end()))
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(vis_btn)
        row_3.addWidget(download_btn)
        row_3.addWidget(range_slider)
        row_3.addStretch()

        # Add bottom border
        border_bottom = QLabel(self)
        border_bottom.setPixmap(QPixmap('./images/'+ THEME + '_bottom.png'))
        border_bottom_row = QHBoxLayout()
        border_bottom_row.addWidget(border_bottom)

        v_box.addLayout(border_top_row)
        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)
        v_box.addLayout(border_bottom_row)

        self.websites_tab.setLayout(v_box)

    def make_programs_tab(self):
        global THEME
        v_box = QVBoxLayout()

        # Add top border
        border_top = QLabel(self)
        border_top.setPixmap(QPixmap('./images/' + THEME + '_top.png'))
        border_top_row = QHBoxLayout()
        border_top_row.addWidget(border_top)

        programs_lbl = QLabel('Programs', self)
        programs_lbl.setObjectName('tab_title')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(programs_lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()

        vis_btn = QPushButton(qta.icon('fa.pie-chart',color='orange'),'Visualize Data', self)
        download_btn = QPushButton(qta.icon('fa.download', color='green'),'Download Data', self)
        range_slider = qrangeslider.QRangeSlider()
        vis_btn.clicked.connect(lambda: self.plot_apps(row_2, range_slider.start(), range_slider.end()))
        download_btn.clicked.connect(lambda: self.download_data('app.csv', range_slider.start(), range_slider.end()))
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(vis_btn)
        row_3.addWidget(download_btn)
        row_3.addWidget(range_slider)
        row_3.addStretch()

        # Add bottom border
        border_bottom = QLabel(self)
        border_bottom.setPixmap(QPixmap('./images/'+ THEME + '_bottom.png'))
        border_bottom_row = QHBoxLayout()
        border_bottom_row.addWidget(border_bottom)

        v_box.addLayout(border_top_row)
        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)
        v_box.addLayout(border_bottom_row)

        self.programs_tab.setLayout(v_box)

    def make_help_tab(self):
        # self.scrollArea = QScrollArea(self)
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        # self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 380, 247))
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        v_box = QVBoxLayout()

        # Add top border
        border_top = QLabel(self)
        border_top.setPixmap(QPixmap('./images/' + THEME + '_top.png'))
        border_top_row = QHBoxLayout()
        border_top_row.addWidget(border_top)

        programs_lbl = QLabel('Help', self)
        programs_lbl.setObjectName('tab_title')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(programs_lbl)
        row_1.addStretch()

        general_subtitle = QLabel('General', self)
        general_subtitle.setObjectName('sub-help')
        row_general_subtitle = QHBoxLayout()
        row_general_subtitle.addWidget(general_subtitle)

        q1 = QLabel('1. How can I track my habits through Kitten?', self)
        q1.setObjectName('help')
        row_2 = QHBoxLayout()
        row_2.addWidget(q1)

        q1_answer = QLabel('''
Kitten is a program that tracks and records a variety of user habits on a computer.
It can track how long you spend on a website or application, your mouse movements
and mouse clicks, as well as key presses. It allows you to set preferences and
settings for how the application and device data should be recorded and presented.''', self)
        row_3 = QHBoxLayout()
        row_3.addWidget(q1_answer)

        q2 = QLabel('2. What types of habits does Kitten track?', self)
        q2.setObjectName('help')
        row_4 = QHBoxLayout()
        row_4.addWidget(q2)

        q2_answer = QLabel('''
Kitten allows you to track several different habits, including mouse movements,
mouse clicks, keyboard usage, time spent on applications, and time spent on websites. ''', self)

        row_5 = QHBoxLayout()
        row_5.addWidget(q2_answer)

        q3 = QLabel('3. Can I save the data that Kitten records after I end a tracking session?', self)
        q3.setObjectName('help')
        row_6 = QHBoxLayout()
        row_6.addWidget(q3)

        q3_answer = QLabel('''
Yes. Kitten allows you to download the data from your session so that you can
track your habits.  You can click “Download Data” in any of the data tracking tabs
labeled “Mouse”, “Keyboard”, “Websites”, or “Programs”. ''', self)
        row_7 = QHBoxLayout()
        row_7.addWidget(q3_answer)

        # Add bottom border
        border_bottom = QLabel(self)
        border_bottom.setPixmap(QPixmap('./images/'+ THEME + '_bottom.png'))
        border_bottom_row = QHBoxLayout()
        border_bottom_row.addWidget(border_bottom)

        v_box.addLayout(border_top_row)
        v_box.addLayout(row_1)
        v_box.addLayout(row_general_subtitle)
        v_box.addLayout(row_2)
        v_box.addLayout(row_3)
        v_box.addLayout(row_4)
        v_box.addLayout(row_5)
        v_box.addLayout(row_6)
        v_box.addLayout(row_7)


        v_box.addLayout(border_bottom_row)

        self.help_tab.setLayout(v_box)

    def refresh_images(self):
        pass

    def plot_mouse_loc(self, row, min_time, max_time):
        global mouse_min_time_Stamp
        global mouse_max_time_Stamp
        if row.count() > 2:
            missingBoth = 0
            if not os.path.exists('./data/mouseLoc.csv'):
                 missingBoth+=1
            if not os.path.exists('./data/mouseClicks.csv'):
                 missingBoth+=1

            if missingBoth == 2:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
            else:
                mouse_widget = MyMplCanvas('mouse', min_time, max_time)
                row.replaceWidget(row.itemAt(1).widget(), mouse_widget)

                # time_range_lbl = QLabel(self)
                # print(('/////////////////////////////////:\n' + str(mouse_min_time_Stamp) + ' to ' + str(mouse_max_time_Stamp)))
                # time_range_lbl.setText('Shown range:\n' + str(mouse_min_time_Stamp) + ' to ' + str(mouse_max_time_Stamp))
                # row_2.replaceWidget(row_2.itemAt(1).widget(), time_range_lbl)
        else:
            missingBoth = 0
            if not os.path.exists('./data/mouseLoc.csv'):
                 missingBoth+=1
            if not os.path.exists('./data/mouseClicks.csv'):
                 missingBoth+=1

            if missingBoth == 2:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
            else:
                mouse_widget = MyMplCanvas('mouse', min_time, max_time)
                row.addWidget(mouse_widget)
                row.addStretch()

                # time_range_lbl = QLabel(self)
                # print(('/////////////////////////////////:\n' + str(mouse_min_time_Stamp) + ' to ' + str(mouse_max_time_Stamp)))
                # time_range_lbl.setText('Shown range:\n' + str(mouse_min_time_Stamp) + ' to ' + str(mouse_max_time_Stamp))
                # row_2.addWidget(time_range_lbl)
                # row_2.addStretch()

    def plot_keyboard_input(self, row, min_time, max_time):
        global keyboard_min_time_Stamp
        global keyboard_max_time_Stamp
        if row.count() > 2:
            try:
                kb_widget = MyMplCanvas('keyboard', min_time, max_time)
                row.replaceWidget(row.itemAt(1).widget(), kb_widget)
            except Exception as e:
                print(e)
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
        else:
            try:
                kb_widget = MyMplCanvas('keyboard', min_time, max_time)
                row.addWidget(kb_widget)
                row.addStretch()
            except Exception as e:
                print(e)
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")

    def plot_website(self, row, min_time, max_time):
        if row.count() > 2:
            try:
                web_widget = MyMplCanvas('website', min_time, max_time)
                row.replaceWidget(row.itemAt(1).widget(), web_widget)
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
        else:
            try:
                web_widget = MyMplCanvas('website', min_time, max_time)
                row.addWidget(web_widget)
                row.addStretch()
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")

    def plot_apps(self, row, min_time, max_time):
        if row.count() > 2:
            try:
                app_widget = MyMplCanvas('programs', min_time, max_time)
                row.replaceWidget(row.itemAt(1).widget(), app_widget)
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
        else:
            try:
                app_widget = MyMplCanvas('programs', min_time, max_time)
                row.addWidget(app_widget)
                row.addStretch()
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")

    def initiate_data_collection(self, websites_textbox, programs_textbox, data_stop_btn, data_select_btn):
        # Check for which boxes are ticked and start collecting data for those boxes
        if self.mouse_movement_selection and self.mouse_movement is None:
            self.record_mouse_movement()
        if self.mouse_click_selection and self.mouse_clicks is None:
            self.record_mouse_clicks()
        if self.keyboard_input_selection and self.keyboard is None:
            self.record_keyboard_input()

        ## Programs
        if self.running_program_selection and self.apps is None:
            self.programs_to_record = programs_textbox.text().split(',')
            print("You want to record:", self.programs_to_record)
            print("Recording NOT in sesh")
            self.record_running_programs()
        if self.running_program_selection and self.apps is not None:
            self.programs_to_record = programs_textbox.text().split(',')
            print("You want to record:", self.programs_to_record)
            print("Recording already in sesh")

        ## Websites
        if self.running_website_selection and self.websites is None:
            self.websites_to_record = websites_textbox.text().split(',')
            print("You want to record:", self.websites_to_record)
            print("Recording NOT in sesh")
            self.record_running_websites(self.websites_to_record)
        if self.running_website_selection and self.websites is not None:
            self.websites_to_record = websites_textbox.text().split(',')
            print("You want to record:", self.websites_to_record)
            print("Recording already in sesh") ### SHATS YOU NEED TO REPLACE THIS 'RECORDING IN SESH' WITH STOPPING THE RECORDING AND STARTING A NEW ONE WITH NEW WEBSITES LIST

        data_select_btn.setEnabled(False)
        data_stop_btn.setEnabled(True)


    def stop_data_collection(self, data_stop_btn, data_select_btn):
        if self.mouse_movement is not None:
            self.mouse_movement.recordLoc = False
            self.mouse_movement = None
        if self.mouse_clicks is not None:
            self.mouse_clicks.recordClicks = False
            self.mouse_clicks = None
        if self.keyboard is not None:
            self.keyboard.recordkeyPress = False
            self.keyboard = None
        if self.apps is not None:
            self.apps.recordApps = False
            self.apps = None
        if self.websites is not None:
            self.websites.disableProxy()
            time.sleep(1)
            self.websites.getLog()
            self.websites = None
        if self.keyboard is not None:
            self.keyboard = None
        data_stop_btn.setEnabled(False)
        data_select_btn.setEnabled(True)

    def record_mouse_movement(self):
        # # initialize all event triggers to be clear (don't record anything)

        # create mouseListener thread
        self.mouse_movement = mouseClickAndLocation.MOUSETHREAD(getScreenSize())
        self.mouse_movement.recordScroll = False
        self.mouse_movement.recordClicks = False
        self.mouse_movement.recordLoc = False
        self.mouse_movement.start()

        # turn on all event triggers
        self.mouse_movement.recordLoc = True

    def record_mouse_clicks(self):
        # # initialize all event triggers to be clear (don't record anything)

        # create mouseListener thread
        self.mouse_clicks = mouseClickAndLocation.MOUSETHREAD(getScreenSize())
        self.mouse_clicks.recordScroll = False
        self.mouse_clicks.recordClicks = False
        self.mouse_clicks.recordLoc = False
        self.mouse_clicks.start()

        # turn on all event triggers
        self.mouse_clicks.recordClicks = True

    def record_keyboard_input(self):
        self.keyboard = keyboardTracking.KeyboardThread()
        self.keyboard.recordkeyPress = False;
        self.keyboard.recordkeyRelease = False;
        self.keyboard.start()
        self.keyboard.recordkeyPress = True;

    def record_running_programs(self):
        # UPDATE THIS!!!!
        # initialize all event triggers to be clear (don't record anything)
        stopFlag = threading.Event()
        self.apps = appScript.AppThread(stopFlag)
        self.apps.recordApps = True
        self.apps.start()

    def record_running_websites(self, websites_to_record):
        print('Recording running websites')
        website_string = ''
        for website in websites_to_record:
            website_string += website + " "
        website_string = website_string.rstrip()
        print("website_string looks like: " + website_string)
        self.websites = proxyClient.ProxyClient('167.99.61.206', 8080, website_string)
        self.websites.enableProxy()

    # Functions used to change the state of whether or not user wants data recorded #
    # Used in check boxes #
    def switch_mouse_movement_state(self):
        self.mouse_movement_selection = not self.mouse_movement_selection

    def switch_mouse_click_state(self):
        self.mouse_click_selection = not self.mouse_click_selection

    def switch_keyboard_input_state(self):
        self.keyboard_input_selection = not self.keyboard_input_selection

    def switch_running_program_state(self):
        if self.programs_le.isEnabled():
            self.programs_le.setEnabled(False)
        else:
            self.programs_le.setEnabled(True)
        self.running_program_selection = not self.running_program_selection

    def switch_running_website_state(self):
        if self.websites_le.isEnabled():
            self.websites_le.setEnabled(False)
        else:
            self.websites_le.setEnabled(True)
        self.running_website_selection = not self.running_website_selection

    def download_data(self, data_name, min_time, max_time):
        fileName = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        if fileName:
            try:
                if data_name == 'mouseLoc.csv':
                    # both exist
                    if os.path.exists('./data/mouseLoc.csv') and os.path.exists('./data/mouseClicks.csv'):
                        [loc, clicks, a, b] = getLocAndClicksDF(min_time, max_time)
                        loc.to_csv(fileName + '/' + 'mouseLoc.csv')
                        clicks.to_csv(fileName + '/' + 'mouseClicks.csv')
                    else:
                        if os.path.exists('./data/mouseLoc.csv'): # Just locations
                            [loc, a, b] = getLocDF(min_time, max_time)
                            loc.to_csv(fileName + '/' + 'mouseLoc.csv')
                        else: # Just Clicks
                            [clicks, a, b] = getClicksDF(min_time, max_time)
                            clicks.to_csv(fileName + '/' + 'mouseClicks.csv')
                if data_name == 'keyboard.csv':
                    [keys, a, b] = getKeysDF(min_time, max_time)
                    keys.to_csv(fileName + '/' + 'keyboard.csv')
                if data_name == 'app.csv':
                    [apps, a, b] = getAppDF(min_time, max_time)
                    apps.to_csv(fileName + '/' + 'app.csv')
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before downloading.")

def getClicksDF(min_time, max_time):
    # Read in from .csv
    [clicksAll, lastTime, firstTime]  = csvImport.read_from_CSV('./data/mouseClicks.csv')
    timeDifference = lastTime - firstTime

    # print(locAll) # print data being used
    print("Total time over df = " + str(timeDifference))
    print("First time = " + str(firstTime))
    min_time_Stamp = datetime.datetime.fromtimestamp(min_time * timeDifference/999 + firstTime)
    max_time_Stamp = datetime.datetime.fromtimestamp(max_time * timeDifference/999 + firstTime)
    print("Minimum time = " + str(min_time_Stamp))
    print("Maximum time = " + str(max_time_Stamp))

    # Make new dataframe to plot with limited time
    clicks = clicksAll[clicksAll['Time'].between(min_time, max_time)]
    print(clicks)
    return clicks, min_time_Stamp, max_time_Stamp

def getLocDF(min_time, max_time):
    # Read in from .csv
    [locAll, lastTime, firstTime]  = csvImport.read_from_CSV('./data/mouseLoc.csv')
    timeDifference = lastTime - firstTime

    # print(locAll) # print data being used
    print("Total time over df = " + str(timeDifference))
    print("First time = " + str(firstTime))
    min_time_Stamp = datetime.datetime.fromtimestamp(min_time * timeDifference/999 + firstTime)
    max_time_Stamp = datetime.datetime.fromtimestamp(max_time * timeDifference/999 + firstTime)
    print("Minimum time = " + str(min_time_Stamp))
    print("Maximum time = " + str(max_time_Stamp))

    # Make new dataframe to plot with limited time
    loc = locAll[locAll['Time'].between(min_time_Stamp, max_time_Stamp)]
    print(loc)
    return loc, min_time_Stamp, max_time_Stamp

def getLocAndClicksDF(min_time, max_time):
    [locAll, lastTimeLoc, firstTimeLoc]  = csvImport.read_from_CSV('./data/mouseLoc.csv')
    [clicksAll, lastTimeClicks, firstTimeClicks]  = csvImport.read_from_CSV('./data/mouseClicks.csv')
    firstTime = min(firstTimeLoc, firstTimeClicks)
    lastTime = max(lastTimeLoc, lastTimeClicks)
    timeDifference = lastTime - firstTime

    print('\n')
    print('GRAPHING RANGES -------------------------------------------')
    print("First time = " + str(firstTime))
    print("Last time = " + str(lastTime))
    print("Total time over both clicks and locations = " + str(timeDifference))
    min_time_Stamp = datetime.datetime.fromtimestamp(min_time * timeDifference/999 + firstTime)
    max_time_Stamp = datetime.datetime.fromtimestamp(max_time * timeDifference/999 + firstTime)
    print("Bottom range time = " + str(min_time_Stamp))
    print("Top range time = " + str(max_time_Stamp))

    # Make new dataframe to plot with limited time
    loc = locAll[locAll['Time'].between(min_time_Stamp, max_time_Stamp)]
    print('\nLOCATIONS GRAPHED -------------------------------------------')
    print(loc)
    clicks = clicksAll[clicksAll['Time'].between(min_time_Stamp, max_time_Stamp)]
    print('\nCLICKS GRAPHED -------------------------------------------')
    print(clicks)

    return loc, clicks, min_time_Stamp, max_time_Stamp

def getAppDF(min_time, max_time):
    # Get data from .csv
    [appsAll, lastTime, firstTime]  = csvImport.read_from_CSV('./data/app.csv')
    timeDifference = lastTime - firstTime

    # Narrow down data to appropriate time window
    print('\n')
    print('GRAPHING RANGES -------------------------------------------')
    print("First time = " + str(firstTime))
    print("Last time = " + str(lastTime))
    print("Total time over both clicks and locations = " + str(timeDifference))
    min_time_Stamp = datetime.datetime.fromtimestamp(min_time * timeDifference/999 + firstTime)
    max_time_Stamp = datetime.datetime.fromtimestamp(max_time * timeDifference/999 + firstTime)
    print("Bottom range time = " + str(min_time_Stamp))
    print("Top range time = " + str(max_time_Stamp))

    # Make new dataframe to plot with limited time
    apps = appsAll[appsAll['Time'].between(min_time_Stamp, max_time_Stamp)]
    print('APPS GRAPHED -------------------------------------------')
    print(apps)

    return apps, min_time_Stamp, max_time_Stamp

def getKeysDF(min_time, max_time):
    # Get data from .csv
    [keysAll, lastTime, firstTime]  = csvImport.read_from_CSV('./data/keyboard.csv')
    timeDifference = lastTime - firstTime

    # Narrow down data to appropriate time window
    print('\n')
    print('GRAPHING RANGES -------------------------------------------')
    print("First time = " + str(firstTime))
    print("Last time = " + str(lastTime))
    print("Total time over both clicks and locations = " + str(timeDifference))
    min_time_Stamp = datetime.datetime.fromtimestamp(min_time * timeDifference/999 + firstTime)
    max_time_Stamp = datetime.datetime.fromtimestamp(max_time * timeDifference/999 + firstTime)
    print("Bottom range time = " + str(min_time_Stamp))
    print("Top range time = " + str(max_time_Stamp))

    # Make new dataframe to plot with limited time
    keys = keysAll[keysAll['Time'].between(min_time_Stamp, max_time_Stamp)]
    print('\KEYS GRAPHED -------------------------------------------')
    print(keys)

    return keys, min_time_Stamp, max_time_Stamp

def getScreenSize():
    ''' Returns screen size '''
    screen = app.primaryScreen()
    screenSize = screen.size()
    # print('Detecting resolution...\nwidth: %d \nheight: %d' % (screenSize.width(), screenSize.height()))
    return screen.size()

if __name__ == '__main__':
    if not os.path.exists('./data'):
        os.makedirs('./data')
    app = QApplication(sys.argv)
    getScreenSize()
    ex = App()
    sys.exit(app.exec_())
