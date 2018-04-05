from pynput import mouse
import os.path
import csv as c
import time
import datetime

csvPath = './data/'

class MOUSETHREAD(mouse.Listener):
    """
    I made my own class that is the child of mouse.Listener. Every time a click, movement, or scroll occurs, the
    appropriate function name is executed. This is in a thread, so it can happen in parallel with the calling script
    """

    # initialize the class
    def __init__(self):
        # initializes mouse.Listener
        super().__init__(on_move = self.on_move, on_click = self.on_click, on_scroll = self.on_scroll)
        self.t = 0
        self.x = 0
        self.y = 0


        # initializes the recording booleans to false
        self.recordLoc = False
        self.recordClicks = False
        self.recordScroll = False
        self.firstClickTime = 0
        self.firstMoveTime = 0

        if os.path.exists(csvPath + 'mouseLoc.csv'):
            with open(csvPath + 'mouseLoc.csv') as f:
                reader = c.reader(f)
                row1 = next(reader)
                row2 = next(reader)
                self.firstMoveTime = float(row2[0])

        if os.path.exists(csvPath + 'mouseClicks.csv'):
            with open(csvPath + 'mouseClicks.csv') as f:
                reader2 = c.reader(f)
                row1 = next(reader2)
                row2 = next(reader2)
                self.firstClickTime = float(row2[0])

    # called when mouse moves
    def on_move(self, x, y):
        self.x = x
        self.y = y
        if self.recordLoc:
            self.t = time.time()
            print('Pointer moved to {0}'.format((self.x, self.y)) + ' at ' + str(datetime.datetime.fromtimestamp(self.t)))
            self.t = round((self.t - self.firstMoveTime), 7)
            self.write_csv('mouseLoc.csv', str(self.t)  + ',' + str(self.x) + ',' + str(self.y) + '\n')

    # called when mouse clicks
    def on_click(self, x, y, button, pressed):
        self.x = x
        self.y = y
        self.t = round((time.time() - self.firstClickTime), 7)
        if self.recordClicks:
            if pressed:
                words = str(self.t) + ',' + 'p,' + str(self.x) + ',' + str(y)
            else:
                words = str(self.t) + ',' + 'r,' + str(self.x) + ',' + str(y)
            print(words)
            self.write_csv('mouseClicks.csv', words + '\n') # prints p if pressed and r if released

    # called when mouse moves
    def on_scroll(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.t = round(time.time(), 7)
        if self.recordScroll:
            print('Scrolled {0} at {1}'.format(
                'down' if dy < 0 else 'up',
                (x, y)))
        # print???

    # writes to .csv file in real time
    def write_csv(self, csv, words):
        # If the file doesn't exist, make proper column titles
        if not os.path.exists(csvPath + csv):
            if(csv == 'mouseLoc.csv'):
                self.firstMoveTime = self.t
                with open(csvPath + csv, 'a') as f:
                    f.write('Time,x,y\n')
            if(csv == 'mouseClicks.csv'):
                self.firstClickTime = self.t
                with open(csvPath + csv, 'a') as f:
                    f.write('Time,Pressed/Released,x,y\n')

        # Write data to file
        with open(csvPath + csv, 'a') as f:
            f.write(words)
