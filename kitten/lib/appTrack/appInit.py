import appTracking as app
import time

if __name__ == '__main__':
    # initialize all event triggers to be clear (don't record anything)

    # create mouseListener thread
    my_apps = app.AppThread()
    my_apps.get_data()

    time.sleep(2)
