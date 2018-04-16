from pynput import keyboard
import os.path
import time
import datetime
import csv as c

csvPath = './data/'

class KeyboardThread(keyboard.Listener):
    '''
    This class is the child of keyboard.Listener. Every time a key is pressed, the
    appropriate function name is executed. This is in a thread, so it can happen in parallel with the calling script.
    Something to note is that the first entry in the time column is a timestamp of time since epoch. All other entries
    are the time in seconds since the first entry. This was done to conserve space. A function defined in
    csvToDataFrameExample takes this format and transforms it all into timestamps.
    '''

    def __init__(self):
        '''
        This constructor initiates the super class and all class variables as well
        as gets the firstTypeTime from the .csv file
        '''

        # initialize keyboard.Listener
        super().__init__(on_press=self.on_press, on_release=self.on_release)

        self.recordkeyPress = False
        self.recordkeyRelease = False
        self.firstTypeTime = 0

        if os.path.exists(csvPath + 'keyboard.csv'):
            with open(csvPath + 'keyboard.csv') as f:
                reader = c.reader(f)
                row1 = next(reader)
                row2 = next(reader)
                self.firstTypeTime = float(row2[0])

    def on_press(self,key):
        '''
        Every time a key is pressed, this executes. The key is identified and the
        time is recorded to a .csv file
        '''
        if self.recordkeyPress: # if recording is enabled
            self.t = time.time()
            try:
                #words = 'alphanumeric key {0} pressed'.format(key.char)
                if('{0}'.format(key.char) == ','):
                    print(str(datetime.datetime.fromtimestamp(self.t)) + ', ' + 'p, comma')
                    self.t = round((self.t - self.firstTypeTime), 7)
                    words = str(self.t) + ', ' + 'p, comma'
                else:
                    print(str(datetime.datetime.fromtimestamp(self.t)) + ', ' + 'p, {0}'.format(key.char))
                    self.t = round((self.t - self.firstTypeTime), 7)
                    words = str(self.t) + ', ' + 'p, {0}'.format(key.char)
            except AttributeError:
                #words = 'special key {0} pressed'.format(key)
                if('{0}'.format(key)[4:] == ','):
                    print(str(datetime.datetime.fromtimestamp(self.t)) + ', ' + 'p, ' +'comma')
                    self.t = round((self.t - self.firstTypeTime), 7)
                    words = str(self.t) + ', ' + 'p, ' + 'comma'
                else:
                    print(str(datetime.datetime.fromtimestamp(self.t)) + ', ' + 'p, ' + '{0}'.format(key)[4:])
                    self.t = round((self.t - self.firstTypeTime), 7)
                    words = str(self.t) + ', ' + 'p, ' + '{0}'.format(key)[4:]

            self.write_csv('keyboard.csv', words + '\n')  # prints p if pressed

    def on_release(self,key):
        '''
        Every time a key is released, this executes. The key is identified and the
        time is recorded to a .csv file
        '''
        if self.recordkeyRelease:
            self.t = time.time()
            try:
                #words = '{0} released'.format(key.char)
                print(str(datetime.datetime.fromtimestamp(self.t)) + ', ' + 'r, {0}'.format(key.char))
                self.t = round((self.t - self.firstTypeTime), 7)
                words = str(self.t) + ', ' + 'r, {0}'.format(key.char)
            except AttributeError:
                #words = '{0} released'.format(key)
                print(str(datetime.datetime.fromtimestamp(self.t)) + ', ' + 'r, ' + '{0}'.format(key)[4:])
                self.t = round((self.t - self.firstTypeTime), 7)
                words = str(self.t) + ', ' + 'r, ' + '{0}'.format(key)[4:]
            self.write_csv('keyboard.csv', words + '\n')  # prints r if released

    def write_csv(self, csv, words):
        '''
        This writes to keyboard.csv the appropriate string containing information on
        what key was pressed/released, whether it was pressed or released, and the
        time that it was pressed/released
        '''
        if not os.path.exists(csvPath + csv):
            self.firstTypeTime = self.t
            if(csv == 'keyboard.csv'):
                with open(csvPath + csv, 'a') as f:
                    f.write('Time,Pressed/Released,Key\n')
        with open(csvPath + csv, 'a') as f:
            f.write(words)
