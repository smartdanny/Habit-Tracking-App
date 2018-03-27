from pynput import keyboard
import os.path
import time

csvPath = '../../data/'

class KeyboardThread(keyboard.Listener):


    def __init__(self):
        # initialize keyboard.Listener
        super().__init__(on_press=self.on_press, on_release=self.on_release)

        self.recordkeyPress = False;
        self.recordkeyRelease = False;

    def on_press(self,key):
        t = time.time()
        if self.recordkeyPress:
            try:
                #words = 'alphanumeric key {0} pressed'.format(key.char)
                words = str(t) + ', ' + 'p, {0}'.format(key.char)
            except AttributeError:
                #words = 'special key {0} pressed'.format(key)
                words = str(t) + ', ' + 'p, {0}'.format(key)[7:]
            print(words)
            self.write_csv('keyboard.csv', words + '\n')  # prints p if pressed

    def on_release(self,key):
        t = time.time()
        if self.recordkeyRelease:
            try:
                #words = '{0} released'.format(key.char)
                words = str(t) + ', ' + 'r, {0}'.format(key.char)
            except AttributeError:
                #words = '{0} released'.format(key)
                words = str(t) + ', ' + 'r, {0}'.format(key)[7:]
            print(words)
            self.write_csv('keyboard.csv', words + '\n')  # prints r if released

    # writes to .csv file in real time
    def write_csv(self, csv, words):
        if not os.path.exists(csvPath + csv):
            if(csv == 'keyboard.csv'):
                with open(csvPath + csv, 'a') as f:
                    f.write('Time,Pressed/Released,Key\n')
        with open(csvPath + csv, 'a') as f:
            f.write(words)