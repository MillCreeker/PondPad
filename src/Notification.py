from win10toast import ToastNotifier
import time
import Config

def show(title: str, message: str, consultSettings:bool=True):
    if (consultSettings == True):
        settings = Config.get_settings()
        if (settings['showNotifications'] == False):
            return
    
    try:
        toaster = ToastNotifier()
        toaster.show_toast(
            title,
            message,
            './icons/icon.ico',
            duration=5,
            threaded=True)
        time.sleep(0.1)
    except:
        pass