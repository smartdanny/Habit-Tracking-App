from ctypes import windll, Structure, c_long, byref

class MOUSE(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = MOUSE()
    windll.user32.GetCursorPos(byref(pt))
    return {pt.x, pt.y}

def write_Pos():
    with open('mouseData.csv', 'a') as f:     #append to file
        f.write(str(x) + ","  + str(y) + '\n')



####################################MAIN##########################
x, y = queryMousePosition()
print(str(x) + ", " + str(y))
write_Pos()

