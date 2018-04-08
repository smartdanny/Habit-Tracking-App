import requests
import time
import winreg
import platform

class ProxyClient:
    '''
    The proxy client connects to the web server that runs Kitten's forward web proxy.
    The user chooses which websites he or she would like to track. The ProxyClient object
    receives the amount of times these websites are accessed, which is saved in a .csv file.

    self.host: The web server's IP address that runs the web proxy
    self.port: The web server's port that serves the log information
    self.website: A space delimited string that holds the websites the user wishes to track
    '''

    def __init__(self, host, port):
        self.server_host = host
        self.server_port = port
        self.os = platform.system()

    def enableProxy(self):
        if (self.os == 'Windows'):
            print("OS: " + self.os)

            INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                0, winreg.KEY_ALL_ACCESS)

            def set_key(name, value):
                _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
                winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)

            set_key('ProxyEnable', 1)
            set_key('ProxyServer', u'167.99.61.206:3128')
            print("Proxy enabled...")

    def disableProxy(self):
        if (self.os == 'Windows'):

            INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                0, winreg.KEY_ALL_ACCESS)

            def set_key(name, value):
                _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
                winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)
                
            set_key('ProxyEnable', 0)
            print("Proxy disabled...")

    def getWebsites(self):
        self.websites = input("Please enter the websites that you would like to track the usage of: ")

    def getLog(self):
        try:
            response = requests.post('http://' + self.server_host + ':' + str(self.server_port), data=self.websites)
        except ConnectionError:
            print("Unable to connect with Kitten server...")

        with open('website_log.csv', 'a') as log:
            log.write(response.text)

if __name__ == '__main__':
    client = ProxyClient('167.99.61.206', 8080) # immediately fires off when the user begins tracking website usage
    client.getWebsites() # should take in the websites that the user lists in the GUI
    client.enableProxy() # based on the OS, the proxy settings will immediately be enabled for browsers
    print("Tracking website usage...")
    for i in range(15): # have proxy run for 15 seconds - should last until user stops tracking session
        print(i+1)
        time.sleep(1)
    client.disableProxy() # once user stops session, the proxy settings will be disabled
    client.getLog() # client then sends POST request that receives csv data
    print("Logging information added to website_log.csv...")
