from GamePad import GamePad
from Converter import Converter
import Notification
from Tray import Tray
import time
import threading
import os

if __name__ == '__main__':
    try:
        gp = GamePad()
        
        converter = Converter('layout')
        time.sleep(0.1)
        
        Tray = Tray() 
        Tray.create()
        while True:
            is_monitoring_input = False
            for thread in threading.enumerate():
                if (thread.name == 'Monitor'):
                    is_monitoring_input = True
                    break
            
            if (is_monitoring_input == False):
                os._exit(0)
            
            input = gp.read()
            converter.convert(input)
    
    except FileNotFoundError:
        Notification.show(
            'Necessary files missing',
            ' ',
            False
        )
        os._exit(0)