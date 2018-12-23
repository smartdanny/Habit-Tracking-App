import os.path
import time
import csv as c
import subprocess
import threading


csvPath = './data/'
# You probably need to use the row below this instead
#csvPath = './data/''

class AppThread(threading.Thread):

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.firstTypeTime = 0
        self.recordApps = False
        self.stopped = event

        if os.path.exists(csvPath + 'app.csv'):
            with open(csvPath + 'app.csv') as f:
                reader = c.reader(f)
                row1 = next(reader)
                row2 = next(reader)
                self.firstTypeTime = float(row2[0])

    def run(self):
        while self.recordApps:
            self.t = round((time.time() - self.firstTypeTime), 7)
            process=subprocess.Popen(["powershell","gps | ? {$_.mainwindowhandle -ne 0} | select name"],stdout=subprocess.PIPE);
            result=process.communicate()[0].decode("utf-8")
            result = result.replace(" ", "")
            result = result.strip("\r\nName\r\n---")
            temp_t = self.t
            if self.firstTypeTime == 0:
                temp_t = 0
            result = "\n" + str(self.t) + "," + result.replace("\r\n", "\n" + str(temp_t) + ",")
            print (result)
            self.write_csv('app.csv',result)
            time.sleep(3)

    def write_csv(self, csv, words):
        '''
        This writes to app.csv the appropriate string containing information on
        what key was pressed/released, whether it was pressed or released, and the
        time that it was pressed/released
        '''
        if not os.path.exists(csvPath + csv):
            self.firstTypeTime = self.t
            if(csv == 'app.csv'):
                with open(csvPath + csv, 'a') as f:
                    f.write('Time,App')
        with open(csvPath + csv, 'a') as f:
            f.write(words)
