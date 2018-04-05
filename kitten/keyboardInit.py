import lib.keyboardTrack.keyboardTracking as keys
import time

if __name__ == '__main__':
    # initialize all event triggers to be clear (don't record anything)

    # create mouseListener thread
    keyboard = keys.KeyboardThread()
    keyboard.recordkeyPress = False;
    keyboard.recordkeyRelease = False;
    keyboard.start()

    keyboard.recordkeyPress = True;
    keyboard.recordkeyRelease = True;

    time.sleep(2)
    keyboard.stop()
