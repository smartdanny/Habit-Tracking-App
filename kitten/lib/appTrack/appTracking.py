import os.path
import time
import datetime
import csv as c
import subprocess;
csvPath = './'

class AppThread():

    def __init__(self):
        get_data = self.get_data

        self.firstTypeTime = 0

        if os.path.exists(csvPath + 'app.csv'):
            with open(csvPath + 'app.csv') as f:
                reader = c.reader(f)
                row1 = next(reader)
                row2 = next(reader)
                self.firstTypeTime = float(row2[0])

    def get_data(self):
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

    def write_csv(self, csv, words):
        '''
        This writes to keyboard.csv the appropriate string containing information on
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