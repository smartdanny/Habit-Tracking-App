import winreg
import platform
import time

os = platform.system()

if (os == 'Windows'):
    print("OS: " + os)

    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
        0, winreg.KEY_ALL_ACCESS)

    def set_key(name, value):
        _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
        winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)

    set_key('ProxyEnable', 1)
    set_key('ProxyServer', u'167.99.61.206:3128')
    print("Proxy enabled...")

for i in range(5):
    print(i+1)
    time.sleep(1)

if (os == 'Windows'):
    set_key('ProxyEnable', 0)
    print("Proxy disabled...")
