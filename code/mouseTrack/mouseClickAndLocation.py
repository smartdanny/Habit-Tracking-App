from pynput import mouse


class MOUSETHREAD(mouse.Listener):
    """
    I made my own class that is the child of mouse.Listener. Every time a click, movement, or scroll occurs, the
    appropriate function name is executed. This is in a thread, so it can happen in parallel with the calling script
    """

    # initialize the class
    def __init__(self):
        # initializes mouse.Listener
        super().__init__(on_move = self.on_move, on_click = self.on_click, on_scroll = self.on_scroll)

        # initializes the recording booleans to false
        self.recordLoc = False
        self.recordClicks = False
        self.recordScroll = False

        self.x = 0
        self.y = 0

    # called when mouse moves
    def on_move(self, x, y):
        self.x = x
        self.y = y
        if self.recordLoc:
            print('Pointer moved to {0}'.format(
                (self.x, self.y)))
            # self.write_csv('mouseLoc.csv', str(self.x) + ', ' + str(self.y) + '\n')

    # called when mouse clicks
    def on_click(self, x, y, button, pressed):
        self.x = x
        self.y = y
        if self.recordClicks:
            if pressed:
                words = 'p ' + str(self.x) + ', ' + str(y)
            else:
                words = 'r ' + str(self.x) + ', ' + str(y)
            print(words)
            # self.write_csv('mouseClicks.csv', words + '\n')  # prints p if pressed and r if released

    # called when mouse moves
    def on_scroll(self, x, y, dx, dy):
        self.x = x
        self.y = y
        if self.recordScroll:
            print('Scrolled {0} at {1}'.format(
                'down' if dy < 0 else 'up',
                (x, y)))
        # print???

    # writes to .csv file in real time
    # def write_csv(self, csv, words):
        # with open(csv, 'a') as f:
        #     f.write(words)
