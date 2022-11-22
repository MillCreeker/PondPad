from inputs import get_gamepad
import math
import threading
import Notification

class GamePad():
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    class Input():
        JoystickLeftX = 0
        JoystickLeftY = 0
        JoystickRightX = 0
        JoystickRightY = 0
        TriggerLeft = 0
        TriggerRight = 0
        BumperLeft = 0
        BumperRight = 0
        A = 0
        B = 0
        X = 0
        Y = 0
        ThumbLeft = 0
        ThumbRight = 0
        Start = 0
        Select = 0
        DPadLeft = 0
        DPadRight = 0
        DPadUp = 0
        DPadDown = 0
    
    def __init__(self):
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.name = 'Monitor'
        self._monitor_thread.start()

    def read(self):
        return self.Input

    def _monitor_controller(self):
        while True:
            events = []
            try:
                events = get_gamepad()
            except:
                try:
                    Notification.show(
                        'No Gamepad connected',
                        'Please connect a supported gamepad and relaunch Pond Pad',
                    )
                    return
                except:
                    return
            
            for event in events:
                if event.code == 'ABS_X':
                    self.Input.JoystickLeftX = event.state / GamePad.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Y':
                    self.Input.JoystickLeftY = event.state / GamePad.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.Input.JoystickRightX = event.state / GamePad.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.Input.JoystickRightY = event.state / GamePad.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    if (event.state > 0.1):
                        self.Input.TriggerLeft = 1
                    else:
                        self.Input.TriggerLeft = 0
                    # self.Input.TriggerLeft = event.state / GamePad.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    if (event.state > 0.1):
                        self.Input.TriggerRight = 1
                    else:
                        self.Input.TriggerRight = 0
                    # self.Input.TriggerRight = event.state / GamePad.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.Input.BumperLeft = event.state
                elif event.code == 'BTN_TR':
                    self.Input.BumperRight = event.state
                elif event.code == 'BTN_SOUTH':
                    self.Input.A = event.state
                elif event.code == 'BTN_EAST':
                    self.Input.B = event.state
                elif event.code == 'BTN_WEST':
                    self.Input.X = event.state
                elif event.code == 'BTN_NORTH':
                    self.Input.Y = event.state
                elif event.code == 'BTN_THUMBL':
                    self.Input.ThumbLeft = event.state
                elif event.code == 'BTN_THUMBR':
                    self.Input.ThumbRight = event.state
                elif event.code == 'BTN_START':
                    self.Input.Start = event.state
                elif event.code == 'BTN_SELECT':
                    self.Input.Select = event.state
                elif event.code == 'ABS_HAT0X':
                    if (event.state == 1):
                        self.Input.DPadLeft = 0
                        self.Input.DPadRight = 1
                    elif (event.state == -1):
                        self.Input.DPadLeft = 1
                        self.Input.DPadRight = 0
                    else:
                        self.Input.DPadLeft = 0
                        self.Input.DPadRight = 0
                elif event.code == 'ABS_HAT0Y':
                    if (event.state == 1):
                        self.Input.DPadUp = 0
                        self.Input.DPadDown = 1
                    elif (event.state == -1):
                        self.Input.DPadUp = 1
                        self.Input.DPadDown = 0
                    else:
                        self.Input.DPadUp = 0
                        self.Input.DPadDown = 0