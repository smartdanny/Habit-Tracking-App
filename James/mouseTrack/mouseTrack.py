from ctypes import windll, Structure, c_long, byref
import threading, time

class MOUSE(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

class MouseTracker(threading.Thread):
    def getMousePos(self):
        pt = MOUSE()
        windll.user32.GetCursorPos(byref(pt))
        return {pt.x, pt.y}

    def writePos(self):
        with open('mouseData.csv', 'a') as f:     #append to file
            f.write(str(self.x) + ","  + str(self.y) + '\n')

    #initialize thread event variable
    def __init__(self, recordEvent, exitEvent, sampleRate):
        threading.Thread.__init__(self) #initializes class
        self.sampleRate = sampleRate
        self.recording = recordEvent #passes in external event variable to class
        self.exit = exitEvent

    def run(self):
        while not self.exit.is_set() and self.recording.wait(): #infinte loop as long as recording is set and not stopped
            self.x, self.y = self.getMousePos()
            print(str(self.x) + ", " + str(self.y))
            self.writePos()
            time.sleep(1/self.sampleRate) #sleep for period 1/sampleRate


####################################MAIN####################################
#Defining a threading event to turn on and off mouse tracking
mouseRecording = threading.Event()
mouseRecording.clear() #enable recording for 1 second

#Defining a threading event to exit the thread
exitMouseRecording = threading.Event()
exitMouseRecording.clear()

#Start thread
mouseTrackerThread = MouseTracker(mouseRecording, exitMouseRecording, 60) #pass in recording event, sample 60 fps
mouseTrackerThread.start()


#DEMONSTRATION
mouseRecording.set()
time.sleep(1)
mouseRecording.clear() #stop the thread
time.sleep(5)

#Can turn back on later with...
mouseRecording.set() #enable recording for 1 second
time.sleep(1)
mouseRecording.clear()
exitMouseRecording.set() #stop the thread

