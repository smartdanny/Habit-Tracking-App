import lib.appTrack.appTracking as app
import threading

# if cannot import appTracking, use following line
#import lib.appTrack.appTracking as app

import time

if __name__ == '__main__':
    # initialize all event triggers to be clear (don't record anything)

    # create mouseListener thread
    stopFlag = threading.Event()
    my_apps = app.AppThread(stopFlag)

    my_apps.recordApps = True
    my_apps.start()

    time.sleep(10)

    my_apps.recordApps = False
    time.sleep(5)
