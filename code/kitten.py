import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QCoreApplication
from mouseTrack import mouseClickAndLocation
import time

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('kitten')
        self.setWindowIcon(QIcon('../images/kitten_16'))
        self.setGeometry(100, 100, 300, 200)
        self.home = Home(self)
        self.setCentralWidget(self.home)

        self.show()

class Home(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # initialize tab screen
        self.tabs = QTabWidget()
        self.home_tab = QWidget()
        self.data_select_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.home_tab,"Home")
        self.tabs.addTab(self.data_select_tab,"Data Select")

        self.make_home_tab()
        self.make_data_select_tab()





        self.layout.addWidget(self.tabs)
        # self.setLayout(self.layou)
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
        data_select_btn = QPushButton('select data', self)
        data_select_btn.clicked.connect(QCoreApplication.instance().quit)
        row_3 = QHBoxLayout()
        row_3.addStretch()
        row_3.addWidget(data_select_btn)
        row_3.addStretch()

        # Create quit button, add it to the same row as data selection button.
        quit_btn = QPushButton('quit', self)
        quit_btn.clicked.connect(QCoreApplication.instance().quit)
        row_3.addWidget(quit_btn)
        row_3.addStretch()

        v_box = QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(row_1)
        v_box.addLayout(row_2)
        v_box.addLayout(row_3)
        v_box.addStretch(1) # This takes up space at the bottom.

        self.home_tab.setLayout(v_box)

    def make_data_select_tab(self):
        # creat button to move to data selection page
        data_select_btn = QPushButton('Start Collecting Mouse Data', self)
        data_select_btn.clicked.connect(self.record_mouse)
        row_1 = QHBoxLayout()
        row_1.addStretch()
        row_1.addWidget(data_select_btn)
        row_1.addStretch()

        v_box = QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(row_1)
        v_box.addStretch(1) # This takes up space at the bottom.

        self.data_select_tab.setLayout(v_box)

    def record_mouse(self):
        # # initialize all event triggers to be clear (don't record anything)

        # create mouseListener thread
        mouse = mouseClickAndLocation.MOUSETHREAD()
        mouse.recordScroll = False
        mouse.recordClicks = False
        mouse.recordLoc = False
        mouse.start()

        # wait for 2 seconds (don't record)
        # time.sleep(2)

        # turn on all event triggers and record for 2 seconds
        mouse.recordScroll = True
        mouse.recordClicks = True
        mouse.recordLoc = True
        time.sleep(2)

        # stop thread
        mouse.stop()

        time.sleep(2)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
