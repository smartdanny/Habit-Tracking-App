from pynput import mouse
import os.path
import csv as c
import time
import datetime

csvPath = './data/'

class MOUSETHREAD(mouse.Listener):
    """
    I made my own class that is the child of mouse.Listener. Every time a click, movement, or scroll occurs, the
    appropriate function name is executed. This is in a thread, so it can happen in parallel with the calling script.
    Something to note is that the first entry in the time column is a timestamp of time since epoch. All other entries
    are the time in seconds since the first entry. This was done to conserve space. A function defined in
    csvToDataFrameExample takes this format and transforms it all into timestamps.
    Here is a flowchart that shows the functionality of this class: https://drive.google.com/open?id=1nkjeEaBwpMA4k9E7MTChhutrnZnLYbYx
    """

    # initialize the class
    def __init__(self, screenSize):
        '''
        This constructor initiates the super class and all class variables as well
        as gets the firstMoveTime and firstClickTime from the .csv files
        '''

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

        # Determine maximum value of X and Y
        self.maxX = screenSize.width()
        self.maxY = screenSize.height()

        # If mouseLoc.csv exists, take the first entry and assign it to firstMoveTime
        if os.path.exists(csvPath + 'mouseLoc.csv'):
            with open(csvPath + 'mouseLoc.csv') as f:
                reader = c.reader(f)
                row1 = next(reader)
                row2 = next(reader)
                self.firstMoveTime = float(row2[0])

        # If mouseClicks.csv exists, take the first entry and assign it to firstClickTime
        if os.path.exists(csvPath + 'mouseClicks.csv'):
            with open(csvPath + 'mouseClicks.csv') as f:
                reader2 = c.reader(f)
                row1 = next(reader2)
                row2 = next(reader2)
                self.firstClickTime = float(row2[0])

    def on_move(self, x, y):
        ''' This is called every time the mouse changes location. It writes new location to mouseLoc.csv '''
        self.x = x
        self.y = y
        self.checkLimits()
        if self.recordLoc: # if recording is enabled...
            self.t = time.time() # grab the time since epoch
            print('Pointer moved to {0}'.format((self.x, self.y)) + ' at ' + str(datetime.datetime.fromtimestamp(self.t)))
            self.t = round((self.t - self.firstMoveTime), 7) # calculate difference from first entry
            self.write_csv('mouseLoc.csv', str(self.t)  + ',' + str(self.x) + ',' + str(self.y) + '\n') # write to .csv

    def on_click(self, x, y, button, pressed):
        ''' This is called every time the mouse is pressed or released. It writes new location to mouseClicks.csv '''
        self.x = x
        self.y = y
        self.checkLimits()
        self.t = round((time.time() - self.firstClickTime), 7)
        if self.recordClicks: # if recording is enabled...
            if pressed:
                words = str(self.t) + ',' +  str(self.x) + ',' + str(y)
            else:
                words = str(self.t) + ',' +  str(self.x) + ',' + str(y)
            print(words)
            self.write_csv('mouseClicks.csv', words + '\n') # prints p if pressed and r if released

    def on_scroll(self, x, y, dx, dy):
        ''' This function executes every time the user scrolls. However, we do not utilize it in Kitten '''
        self.x = x
        self.y = y
        self.checkLimits()
        self.t = round(time.time(), 7)
        if self.recordScroll:
            print('Scrolled {0} at {1}'.format(
                'down' if dy < 0 else 'up',
                (x, y)))
        # print???

    def checkLimits(self):
        ''' Makes sure there are no negative values or values outside resolution '''
        if(self.x > self.maxX):
            self.x = self.maxX
        if(self.x < 0):
            self.x = 0
        if(self.y > self.maxY):
            self.y = self.maxY
        if(self.y < 0):
            self.y = 0

    def write_csv(self, csv, words):
        '''
        This function is used to write to a .csv file. csv is the name of the file
        and words is thread string written to the file
        '''

        # If the file doesn't exist, make proper column titles
        if not os.path.exists(csvPath + csv):
            if(csv == 'mouseLoc.csv'):
                self.firstMoveTime = self.t
                with open(csvPath + csv, 'a') as f:
                    f.write('Time,x,y\n')
            if(csv == 'mouseClicks.csv'):
                self.firstClickTime = self.t
                with open(csvPath + csv, 'a') as f:
                    f.write('Time,x,y\n')

        # Write data to file
        with open(csvPath + csv, 'a') as f:
            f.write(words)
