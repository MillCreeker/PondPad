import pystray
from PIL import Image
import Notification
import threading
import time
import os

class Tray:
    def create(self):
        self.__tray_thread = threading.Thread(target=self.__create_icon, args=())
        self.__tray_thread.daemon = True
        self.__tray_thread.name = 'TrayIcon'
        self.__tray_thread.start()

    def destroy(self):
        self.icon.stop()
        
    
    def __create_icon(self):
        image = Image.open('./icons/icon.ico')
        
        self.icon = pystray.Icon('Pond Pad', image, menu=pystray.Menu(
            pystray.MenuItem('Quit Pond Pad', self.__on_stop)
        ))
        
        self.icon.run()
    
    def __on_stop(self):
        Notification.show(
            'Pond Pad has stopped',
            ' '
        )
        time.sleep(0.1)
        self.destroy()
        os._exit(0)