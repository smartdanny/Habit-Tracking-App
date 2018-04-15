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

    def __init__(self, host, port, websites):
        self.server_host = host
        self.server_port = port
        self.os = platform.system()
        self.websites = websites

    def enableProxy(self):
        '''
        Enables the proxy automatically through operating system settings - currently only viable for Windows.
        This function is called at the very beginning of a tracking session.
        '''
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
        '''
        Disables the proxy automatically through operating system settings - currently only viable for Windows.
        This function is called at the very end of a tracking session.
        '''
        if (self.os == 'Windows'):

            INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                0, winreg.KEY_ALL_ACCESS)

            def set_key(name, value):
                _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
                winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)

            set_key('ProxyEnable', 0)
            print("Proxy disabled...")

    def getLog(self):
        '''
        Sends an HTTP POST request to the Kitten server that holds all the proxy logging informationself.
        Writes the response into the websiteLog.csv that is held with the user's data folder.
        '''
        print("Sending POST request to Kitten server...")
        try:
            response = requests.post('http://' + self.server_host + ':' + str(self.server_port), data=self.websites)
        except ConnectionError:
            print("Unable to connect with Kitten server...")
        print("Received response from Kitten server...")
        with open('../../data/websiteLog.csv', 'w') as log:
            log.write(response.text)
