# this file demonstrates how to run mouseClickandLocation

import mouseClickAndLocation
import time


'''
    Thing to change
        - recording and write data in buffers (if necessary)
        - record location in real time (to know how long you stay on one location)
            - alternatively, time stamp each location to know how long it took to get from one to the other
            - alternatively, have a timed function that executes at 60hz and just writes the last value assigned to x, y
                and also move the writing/printing to this timer based function
        - time stamp mouse clicks/releases
'''

if __name__ == '__main__':
    # initialize all event triggers to be clear (don't record anything)

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
