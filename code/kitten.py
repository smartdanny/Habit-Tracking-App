import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QCoreApplication

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('kitten')
        self.setGeometry(0, 0, 300, 200)
        self.home = Home(self)
        self.setCentralWidget(self.home)

        self.show()

class Home(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)


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

    	# creat button to move to data selection page
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

        self.setLayout(v_box)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
