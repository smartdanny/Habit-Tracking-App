# this file demonstrates how to run mouseClickandLocation

import lib.mouseTrack.mouseClickAndLocation as m
import time

if __name__ == '__main__':
    # initialize all event triggers to be clear (don't record anything)

    # create mouseListener thread
    mouse = m.MOUSETHREAD()
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
