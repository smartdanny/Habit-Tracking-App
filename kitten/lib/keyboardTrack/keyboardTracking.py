from pynput import keyboard
import os.path
import time
import datetime
import csv as c

csvPath = './data/'

class KeyboardThread(keyboard.Listener):


    def __init__(self):
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

        if self.recordkeyPress:
            self.t = time.time()
            try:
                #words = 'alphanumeric key {0} pressed'.format(key.char)
                print(str(datetime.datetime.fromtimestamp(self.t)) + ', ' + 'p, {0}'.format(key.char))
                self.t = round((self.t - self.firstTypeTime), 7)
                words = str(self.t) + ', ' + 'p, {0}'.format(key.char)
            except AttributeError:
                #words = 'special key {0} pressed'.format(key)
                print(str(datetime.datetime.fromtimestamp(self.t)) + ', ' + 'p, ' + '{0}'.format(key)[4:])
                self.t = round((self.t - self.firstTypeTime), 7)
                words = str(self.t) + ', ' + 'p, ' + '{0}'.format(key)[4:]

            self.write_csv('keyboard.csv', words + '\n')  # prints p if pressed

    def on_release(self,key):

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

    # writes to .csv file in real time
    def write_csv(self, csv, words):
        if not os.path.exists(csvPath + csv):
            self.firstTypeTime = self.t
            if(csv == 'keyboard.csv'):
                with open(csvPath + csv, 'a') as f:
                    f.write('Time,Pressed/Released,Key\n')
        with open(csvPath + csv, 'a') as f:
            f.write(words)
