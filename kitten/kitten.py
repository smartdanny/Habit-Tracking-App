import sys
sys.path.append('./lib/')
import matplotlib
import lib.mouseTrack.csvToDataFrameExample as csvHelper
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from os.path import expanduser
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,
                            QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QSizePolicy, QInputDialog,
                            QFileDialog, QMessageBox, QLineEdit, QDesktopWidget, QDialog, QGridLayout)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QLinearGradient
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt
from mouseTrack import mouseClickAndLocation
from keyboardTrack import keyboardTracking
import time
import pandas as pd
import numpy as np
import math
import string
import qtawesome as qta
import seaborn as sns
from qrangeslider import qrangeslider


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, type):
        self.screenSize = getScreenSize()
        if type == 'mouse':
            fig = self.compute_mouse()
        elif type == 'keyboard':
            fig = self.compute_keyboard()
        elif type == 'website':
            fig = self.compute_website()
        elif type == 'programs':
            fig = self.compute_programs()
        else: # default to mouse graph -- likely unnecessary
            fig = self.compute_mouse()
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def compute_mouse(self, min_time = 0, max_time = 0):

        # clear figure before graphing
        plt.clf()

        try:
            loc = pd.read_csv('./data/mouseLoc.csv')
            sns.kdeplot(loc.x, loc.y, shade=True, cmap="Oranges_r")
        except:
            pass

        try:
            clicks = pd.read_csv('./data/mouseClicks.csv')
            plt.scatter(clicks.x, clicks.y, c="w", marker="+")
        except:
            pass

        # Set X and Y limits
        plt.ylim(0, self.screenSize.height()) #limits minimum and maximum values on graph to fit screen size
        plt.xlim(0, self.screenSize.width()) #limits minimum and maximum values on graph to fit screen size

        #Flip y axis and change label location
        ax = plt.gca()
        ax.set_ylim(ax.get_ylim()[::-1])
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        g = plt.gcf()  # get current figure
        return g

    def compute_keyboard(self, min_time = 0, max_time = 0):
        keys = pd.read_csv('./data/keyboard.csv')

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
            elif "<" in k or "," in k:
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
        sns.kdeplot(df.x, df.y, shade=True, shade_lowest=False, cmap="Oranges_r", alpha=0.6)
        keyboard = mpimg.imread('./images/keyboard.png')
        plt.imshow(keyboard)
        g = plt.gcf() # get current figure
        return g

    def compute_website(self, min_time = 0, max_time = 0):
        # websites = pd.read_csv('./data/websites.csv')
        # example data, real data read in from csv
        websites = 'Facebook', 'Reddit', 'Canvas', 'GitHub',
        times = [12,11,3,30]

        # clear figure before graphing
        plt.clf()
        # graph onto figure
        cmap = matplotlib.cm.Oranges(np.arange(0.2,1,.1))
        my_circle = plt.Circle( (0,0), 0.7, color='white')
        plt.pie(times, labels=websites, colors=cmap)
        g = plt.gcf() # get current figure
        g.gca().add_artist(my_circle)
        return g

    def compute_programs(self, min_time = 0, max_time = 0):
        # apps = pd.read_csv('./data/programs.csv')
        # example data, real data read in from csv
        apps = 'Steam', 'Google Chrome', 'Photoshop', 'Minesweeper',
        times = [12,11,3.4,22]

        # clear figure before graphing
        plt.clf()
        # graph onto figure
        cmap=matplotlib.cm.Oranges(np.arange(0.2,1,.1))
        my_circle=plt.Circle( (0,0), 0.7, color='white')
        plt.pie(times, labels=apps, colors=cmap)
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
            font: bold Myriad Pro;
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
        self.programs = None
        self.websites = None
        self.keyboard = None

        # local variables to check when data is to be collected
        self.websites_to_record = []
        self.programs_to_record = []

        # initialize tab screen
        self.tabs = QTabWidget()
        self.home_tab = QWidget()
        self.data_select_tab = QWidget()
        self.mouse_movement_tab = QWidget()
        self.mouse_click_tab = QWidget()
        self.keyboard_tab = QWidget()
        self.websites_tab = QWidget()
        self.programs_tab = QWidget()
        self.help_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.home_tab, qta.icon('fa.home'),"Home")
        self.tabs.addTab(self.data_select_tab, qta.icon('fa.list'), "Data Select")
        self.tabs.addTab(self.mouse_movement_tab, qta.icon('fa.mouse-pointer'),"Mouse Movements")
        self.tabs.addTab(self.keyboard_tab, qta.icon('fa.th'),"Keyboard")
        self.tabs.addTab(self.websites_tab, qta.icon('fa.globe'),"Websites")
        self.tabs.addTab(self.programs_tab, qta.icon('fa.desktop'),"Programs")
        self.tabs.addTab(self.help_tab, qta.icon('fa.question-circle'),"Help")

        self.make_home_tab()
        self.make_data_select_tab()
        self.make_mouse_movement_tab()
        self.make_keyboard_tab()
        self.make_websites_tab()
        self.make_programs_tab()
        self.make_help_tab()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def make_home_tab(self):

        # Add above border
        border_top = QLabel(self)
        border_top.setPixmap(QPixmap('./images/border-top.png'))
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

        # Row 3 buttons
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(about_btn)
        row_3.addWidget(quit_btn)
        row_3.addStretch()

        # add version number at the bottom of the GUI
        version_number = QLabel("1.0.0")
        version_number.setAlignment(Qt.AlignRight)
        row_4 = QHBoxLayout()
        row_4.addWidget(version_number)

        # Add above border
        border_bottom = QLabel(self)
        border_bottom.setPixmap(QPixmap('./images/border-bottom.png'))
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

        data_select_title = QLabel('Data Select', self)
        data_select_title.setObjectName('tab_title')
        data_select_title.setAlignment(Qt.AlignLeft)
        row_0 = QHBoxLayout()
        row_0.addWidget(data_select_title)
        row_0.addStretch()

        tab_title_border = QLabel(self)
        tab_title_border.setPixmap(QPixmap('./images/tab-title-border.png'))
        border_row = QHBoxLayout()
        border_row.addWidget(tab_title_border)
        border_row.addStretch()

        mouse_check_box = QCheckBox('Mouse Movements', self)
        mouse_check_box.stateChanged.connect(self.switch_mouse_movement_state)
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(mouse_check_box)
        row_1.addStretch()

        mouse_check_box = QCheckBox('Mouse Clicks', self)
        mouse_check_box.stateChanged.connect(self.switch_mouse_click_state)
        row_2 = QHBoxLayout()
        row_2.addStretch()
        row_2.addWidget(mouse_check_box)
        row_2.addStretch()

        mouse_check_box = QCheckBox('Keyboard', self)
        mouse_check_box.stateChanged.connect(self.switch_keyboard_input_state)
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(mouse_check_box)
        row_3.addStretch()

        mouse_check_box = QCheckBox('Programs', self)
        programs_le = QLineEdit()
        programs_le.setPlaceholderText('Ex: \'slack,photoshop \' ')
        mouse_check_box.stateChanged.connect(self.switch_running_program_state)
        row_4 = QHBoxLayout()
        row_4.addStretch()
        row_4.addWidget(mouse_check_box)
        row_4.addWidget(programs_le)

        mouse_check_box = QCheckBox('Websites', self)
        websites_le = QLineEdit()
        websites_le.setPlaceholderText('Ex: \'facebook.com,twitter.com \' ')
        mouse_check_box.stateChanged.connect(self.switch_running_website_state)
        row_5 = QHBoxLayout()
        row_5.addStretch()
        row_5.addWidget(mouse_check_box)
        row_5.addWidget(websites_le)

        data_stop_btn = QPushButton(qta.icon('fa.stop', color='red'), 'Stop Collecting Data!', self)
        data_stop_btn.setEnabled(False)
        data_select_btn = QPushButton(qta.icon('fa.play',color='green'), 'Begin Collecting Data!', self)
        data_select_btn.clicked.connect(lambda: self.initiate_data_collection(websites_le, programs_le, data_stop_btn, data_select_btn))
        data_stop_btn.clicked.connect(lambda: self.stop_data_collection(data_stop_btn, data_select_btn))
        row_6 = QHBoxLayout()
        row_6.addStretch()
        row_6.addWidget(data_select_btn)
        row_6.addWidget(data_stop_btn)
        row_6.addStretch()

        v_box = QVBoxLayout()
        v_box.addLayout(row_0)
        v_box.addLayout(border_row)
        v_box.addStretch(1)
        v_box.addLayout(row_1)
        v_box.addLayout(row_2)
        v_box.addLayout(row_3)
        v_box.addLayout(row_4)
        v_box.addLayout(row_5)
        v_box.addStretch(1)
        v_box.addLayout(row_6)
        v_box.addStretch(1) # This takes up space at the bottom.

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
        vis_btn = QPushButton(qta.icon('fa.pie-chart',color='orange'),'Visualize Data', self)
        download_btn = QPushButton(qta.icon('fa.download', color='green'),'Download Data', self)
        range_slider = qrangeslider.QRangeSlider()
        vis_btn.clicked.connect(lambda: self.plot_mouse_loc(row_2, range_slider.start(), range_slider.end()))
        download_btn.clicked.connect(lambda: self.download_data('mouseLoc.csv'))


        # row_3 = self.timeInputDialog() #display the box for the start time
        # row_4 = self.timeInputDialog() #display the box for the start time

        row_5 = QHBoxLayout()
        row_5.addStretch()
        row_5.addWidget(vis_btn)
        row_5.addWidget(download_btn)
        row_3.addWidget(range_slider)
        row_5.addStretch()


        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        # v_box.addLayout(row_3)
        # v_box.addStretch(1)
        # v_box.addLayout(row_4)
        # v_box.addStretch(1)
        v_box.addLayout(row_5)

        self.mouse_movement_tab.setLayout(v_box)

    def make_keyboard_tab(self):
        v_box = QVBoxLayout()

        lbl = QLabel(self)
        lbl.setText('Keyboard')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()

        vis_btn = QPushButton(qta.icon('fa.pie-chart',color='orange'),'Visualize Data', self)
        download_btn = QPushButton(qta.icon('fa.download', color='green'),'Download Data', self)
        range_slider = qrangeslider.QRangeSlider()
        vis_btn.clicked.connect(lambda: self.plot_keyboard_input(row_2, range_slider.start(), range_slider.end()))
        download_btn.clicked.connect(lambda: self.download_data('keyboard.csv'))
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(vis_btn)
        row_3.addWidget(download_btn)
        row_3.addWidget(range_slider)
        row_3.addStretch()

        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)

        self.keyboard_tab.setLayout(v_box)

    def make_websites_tab(self):
        v_box = QVBoxLayout()

        lbl = QLabel(self)
        lbl.setText('Websites')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()

        vis_btn = QPushButton(qta.icon('fa.pie-chart',color='orange'),'Visualize Data', self)
        download_btn = QPushButton(qta.icon('fa.download', color='green'),'Download Data', self)
        range_slider = qrangeslider.QRangeSlider()
        vis_btn.clicked.connect(lambda: self.plot_website(row_2, range_slider.start(), range_slider.end()))
        download_btn.clicked.connect(lambda: self.download_data('websites.csv'))
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(vis_btn)
        row_3.addWidget(download_btn)
        row_3.addWidget(range_slider)
        row_3.addStretch()

        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)

        self.websites_tab.setLayout(v_box)

    def make_programs_tab(self):
        v_box = QVBoxLayout()

        lbl = QLabel(self)
        lbl.setText('Programs')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(lbl)
        row_1.addStretch()

        row_2 = QHBoxLayout()
        row_2.addStretch()

        vis_btn = QPushButton(qta.icon('fa.pie-chart',color='orange'),'Visualize Data', self)
        download_btn = QPushButton(qta.icon('fa.download', color='green'),'Download Data', self)
        range_slider = qrangeslider.QRangeSlider()
        vis_btn.clicked.connect(lambda: self.plot_apps(row_2, range_slider.start(), range_slider.end()))
        download_btn.clicked.connect(lambda: self.download_data('programs.csv'))
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(vis_btn)
        row_3.addWidget(download_btn)
        row_3.addWidget(range_slider)
        row_3.addStretch()

        v_box.addLayout(row_1)
        v_box.addStretch(1)
        v_box.addLayout(row_2)
        v_box.addStretch(1)
        v_box.addLayout(row_3)

        self.programs_tab.setLayout(v_box)

    def make_help_tab(self):

        help_lbl = QLabel(self)
        help_lbl.setText('Help')
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(help_lbl)
        row_1.addStretch()

        v_box = QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(row_1)
        v_box.addStretch(1) # This takes up space at the bottom.

        self.help_tab.setLayout(v_box)

    def plot_mouse_loc(self, row, min_time, max_time):
        if row.count() > 2:
            missingBoth = 0
            try:
                loc = pd.read_csv('./data/mouseLoc.csv')
            except:
                missingBoth+=1
            try:
                plt.scatter(clicks.x, clicks.y, c="w", marker="+")
            except:
                missingBoth+=1

            if missingBoth == 2:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
            else:
                mouse_widget = MyMplCanvas('mouse')
                row.replaceWidget(row.itemAt(1).widget(), mouse_widget)
        else:
            missingBoth = 0
            try:
                loc = pd.read_csv('./data/mouseLoc.csv')
            except:
                missingBoth+=1
            try:
                plt.scatter(clicks.x, clicks.y, c="w", marker="+")
            except:
                missingBoth+=1

            if missingBoth == 2:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
            else:
                mouse_widget = MyMplCanvas('mouse')
                row.addWidget(mouse_widget)
                row.addStretch()

    def plot_keyboard_input(self, row, min_time, max_time):
        if row.count() > 2:
            try:
                kb_widget = MyMplCanvas('keyboard')
                row.replaceWidget(row.itemAt(1).widget(), kb_widget)
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
        else:
            try:
                kb_widget = MyMplCanvas('keyboard')
                row.addWidget(kb_widget)
                row.addStretch()
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")

    def plot_website(self, row, min_time, max_time):
        if row.count() > 2:
            try:
                web_widget = MyMplCanvas('website')
                row.replaceWidget(row.itemAt(1).widget(), web_widget)
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
        else:
            try:
                web_widget = MyMplCanvas('website')
                row.addWidget(web_widget)
                row.addStretch()
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")

    def plot_apps(self, row, min_time, max_time):
        if row.count() > 2:
            try:
                app_widget = MyMplCanvas('programs')
                row.replaceWidget(row.itemAt(1).widget(), app_widget)
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before visualizing.")
        else:
            try:
                app_widget = MyMplCanvas('programs')
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
        if self.running_program_selection and self.programs is None:
            self.programs_to_record = programs_textbox.text().split(',')
            print("You want to record:", self.programs_to_record)
            print("Recording NOT in sesh")
            self.record_running_programs()
        if self.running_program_selection and self.programs is not None:
            self.programs_to_record = programs_textbox.text().split(',')
            print("You want to record:", self.programs_to_record)
            print("Recording already in sesh") ### SHATS YOU NEED TO REPLACE THIS 'RECORDING IN SESH' WITH STOPPING THE RECORDING AND STARTING A NEW ONE WITH NEW PROGRAMS LIST

        ## Websites
        if self.running_website_selection and self.websites is None:
            self.websites_to_record = websites_textbox.text().split(',')
            print("You want to record:", self.websites_to_record)
            print("Recording NOT in sesh")
            self.record_running_websites()
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
        if self.programs is not None:
            self.programs = None
        if self.websites is not None:
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

    def download_data(self, data_name):
        fileName = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        if fileName:
            try:
                df = pd.read_csv('./data/' + data_name)
                df.to_csv(fileName + '/' + data_name)
            except:
                QMessageBox.about(self, "Missing Data", "You do not have any data stored in Kitten. Please collect data before downloading.")

def getScreenSize():
    ''' Returns screen size '''
    screen = app.primaryScreen()
    screenSize = screen.size()
    # print('Detecting resolution...\nwidth: %d \nheight: %d' % (screenSize.width(), screenSize.height()))
    return screen.size()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    getScreenSize()
    ex = App()
    sys.exit(app.exec_())
