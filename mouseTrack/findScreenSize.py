# This script finds the screen resolution and prints it out
import ctypes

def screenSize():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print(screensize)
    return screensize

screenSize();
