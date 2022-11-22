import json
import time
import mouse
import pyautogui
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
from pynput.mouse import Button
import Config
from Overlay import Message
import Notification
import os

MIN_MOUSE_INPUT = 0.1
MOUSE_MOVE_DURATION = 0.06
SCROLL_TIME = 0.06
HOLD_TIME = 0.4

class InputObject():
    input = []
    button = None
    type = None
    action = None
    
    def setData(self, input, button: str, type: str, action: str):
        self.input = input
        self.button = button
        self.type = type
        self.action = action

class Converter():
    DELIMITER = None
    COMBINATION = None
    LAYOUT = None
    LAYOUT_SETTINGS = None
    SETTINGS = None
    
    MOUSE_STICK = None
    
    keyboard = None
    mouse = None
    
    mode = None
    plate = None
    
    active_buttons = []
    hold_time = 0
    scroll_time = 0
    
    Message = None
    
    shutting_down = ''
    
    def __init__(self, layout):
        self.__get_layout_config()
        self.__load_layout(layout)
        self.__configure_layout_settings()
        self.SETTINGS = Config.get_settings()
        self.mode = self.__get_first_mode()
        self.plate = self.__get_first_plate()
        
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.Message = Message()
        Notification.show(
            'Pond Pad is all set up',
            ' '
        )
    
    def __get_layout_config(self):
        config_layout = Config.get_layout_options()
        
        self.DELIMITER = config_layout['DELIMITER']
        self.COMBINATION = config_layout['COMBINATION']
    
    def __load_layout(self, layout):
        layout_file = open(f'./config/{layout}.json', encoding='utf-8')
        self.LAYOUT = json.load(layout_file)
        layout_file.close()
    
    def __configure_layout_settings(self):
        self.LAYOUT_SETTINGS = self.LAYOUT['settings']
        if (self.LAYOUT_SETTINGS['mouseLeft'] == None or
            self.LAYOUT_SETTINGS['mouseLeft'] == True):
            self.MOUSE_STICK = 'JoystickLeft'
        else:
            self.MOUSE_STICK = 'JoystickRight'
    
    def __get_first_mode(self):
        modes = self.LAYOUT['modes']
        for mode in modes:
            return mode
    
    def __get_first_plate(self):
        mode = self.__get_mode()
        plates = mode['plates']
        for plate in plates:
            return plate
    
    
    ##############################
    def convert(self, input):
        exiting = self.__handle_exit(input.Select)
        if (exiting == True):
            return
        
        input_arr = self.__get_input_as_array(input)
        
        self.__switch_plate(input_arr)
        
        input_obj = InputObject()
        for inp in input_arr:
            type, action = self.__get_button_mapping(inp)
            input_obj.setData(input, inp, type, action)
                
            if (type == 'mouse'):
                self.__handle_mouse_move(input_obj)
            elif (type == 'scroll'):
                self.__handle_scrolling(input_obj)
            elif (
                type == 'mode' or
                type == 'click' or
                type == 'write' or
                type == 'press' or
                type == 'hold'):
                self.__handle_press(input_obj)
        
        self.__tidy_active_buttons(input_arr)
    ##############################
    
    
    def __get_input_as_array(self, input: list):
            arr = []
            for button in dir(input):
                value = getattr(input, button)
                if (type(value).__name__ != 'int' and
                    type(value).__name__ != 'float'):
                    continue
                if (float(value) > MIN_MOUSE_INPUT or
                    float(value) < -MIN_MOUSE_INPUT):
                    button_name = button
                    
                    # Joystick handling
                    if ('Joystick' in button):
                        button_name = 'Joystick'
                        if ('Left' in button):
                            button_name += 'Left'
                        elif ('Right' in button):
                            button_name += 'Right'
                        else:
                            continue
                        if ('X' in button):
                            if (float(value) > 0):
                                button_name += 'Right'
                            elif (float(value) < 0):
                                button_name += 'Left'
                            else:
                                continue
                        elif ('Y' in button):
                            if (float(value) > 0):
                                button_name += 'Up'
                            elif (float(value) < 0):
                                button_name += 'Down'
                            else:
                                continue
                        else:
                            continue
                    
                    arr.append(button_name)
            
            return arr
    
    def __get_mode(self):
        return self.LAYOUT['modes'][self.mode]

    def __get_plate(self):
        mode = self.__get_mode()
        return mode['plates'][self.plate]
    
    def __get_button_mapping(self, button: str):
        if (button == None):
            return
        
        plate = self.__get_plate()
        
        if ((button in plate) == False):
            return ['not valid', None]
        
        mapping = self.__convert_joystick_input(button)
        
        if (mapping == None):
            mapping = plate[button].split(self.DELIMITER)
        
        type = action = None
        if (len(mapping) == 2):
            type = mapping[0]
            action = mapping[1]
        
        return type, action
    
    def __convert_joystick_input(self, button: str):
        plate = self.__get_plate()
        
        return_none = False
        if (self.MOUSE_STICK in button):
            if ('mouseSpeed' in plate):
                mouse_speed = float(plate['mouseSpeed'])
                if (mouse_speed > 0):
                    type = 'mouse'
                    action = mouse_speed
                else:
                    return_none = True
        else:
            return_none = True
        
        if (return_none == True):
            return None
        return [type, action]

    def __switch_plate(self, input_arr: list):
        self.plate = self.__get_first_plate()
        
        for input in input_arr:
            type, action = self.__get_button_mapping(input)
            if (type == 'plate'):
                self.plate = action
        
        # self.plate = plate
    
    ##########
    # HANDLE #
    ##########
    
    def __handle_exit(self, select):
        sd_msg = self.SETTINGS['shutDownMsg']
        if (select == 1):
            if (self.shutting_down == sd_msg):
                Notification.show(
                    'Pond Pad has stopped',
                    ' '
                )
                os._exit(0)
            
            new_char = sd_msg[len(self.shutting_down):len(self.shutting_down)+1]
            if (new_char == ' '):
                new_char = sd_msg[len(self.shutting_down):len(self.shutting_down)+2]
            self.shutting_down = self.shutting_down + new_char
            self.Message.show(self.shutting_down, .22, True)
            return True
            
        elif (self.shutting_down != ''):
            del_amount = 1
            del_char = self.shutting_down[len(self.shutting_down)-1:len(self.shutting_down)]
            if (del_char == ' '):
                del_amount = 2
            self.shutting_down = self.shutting_down[:-del_amount]
            
            if (self.shutting_down != ''):
                self.Message.show(self.shutting_down, .1, True)
            return True
        
        return False
    
    def __append_active_button(self, button: str):
        if (button == None):
            return
        if ((button in self.active_buttons) == False):
            self.active_buttons.append(button)
    
    def __handle_mouse_move(self, obj: InputObject):
        x = getattr(obj.input, f'{self.MOUSE_STICK}X')*obj.action
        y = -getattr(obj.input, f'{self.MOUSE_STICK}Y')*obj.action
        mouse.move(x, y, absolute=False, duration=MOUSE_MOVE_DURATION)
    
    def __handle_scrolling(self, obj: InputObject):
        exec_time = time.time()
        if ((exec_time - self.scroll_time) < SCROLL_TIME):
            return
        
        plate = self.__get_plate()
        scroll_speed = plate['scrollSpeed']
        
        if (scroll_speed == None or
            scroll_speed <= 0):
            scroll_speed = 1
        
        if (obj.action == 'up'):
            self.mouse.scroll(0, scroll_speed)
        elif (obj.action == 'down'):
            self.mouse.scroll(0, -scroll_speed)
        elif (obj.action == 'left'):
            self.mouse.scroll(-scroll_speed, 0)
        elif (obj.action == 'right'):
            self.mouse.scroll(scroll_speed, 0)
        
        self.scroll_time = time.time()
    
    def __handle_press(self, obj: InputObject):
        if ((obj.button in self.active_buttons) == True):
            if (obj.type == 'hold'):
                exec_time = time.time()
                if ((exec_time - self.hold_time) >= HOLD_TIME):
                    pyautogui.keyDown(obj.action)
            return
        
        if (obj.type == 'mode'):
            self.mode = obj.action
            self.Message.show(obj.action, .2)
        elif (obj.type == 'click'):
            if (hasattr(Button, obj.action)):
                self.mouse.press(Button[obj.action])
        elif (obj.type == 'write'):
            self.keyboard.type(obj.action)
        elif (obj.type == 'press'):
            self.__handle_key_press(obj.action)
        elif (obj.type == 'hold'):
            if (self.hold_time == 0):
                pyautogui.keyDown(obj.action)
                pyautogui.keyUp(obj.action)
                self.hold_time = time.time()
        
        self.__append_active_button(obj.button)
    
    def __handle_key_press(self, action):
        if self.COMBINATION in action:
            keys = action.split(self.COMBINATION)
            for key in keys:
                if (hasattr(Key, key)):
                    self.keyboard.press(Key[key])
                else:
                    pyautogui.keyDown(key)
            
            keys.reverse()
            
            for key in keys:
                if (hasattr(Key, key)):
                    self.keyboard.release(Key[key])
                else:
                    pyautogui.keyUp(key)
        else:
            if (hasattr(Key, action)):
                self.keyboard.press(Key[action])
            else:
                pyautogui.keyUp(action)
    
    
    def __tidy_active_buttons(self, input: list):
        current_buttons = []
        
        for button in self.active_buttons:
            if ((button in input) == True):
                current_buttons.append(button)
            else:
                type, action = self.__get_button_mapping(button)
                
                if (type == 'click'):
                    if (hasattr(Button, action)):
                        self.mouse.release(Button[action])
                elif (type == 'press'):
                    if (hasattr(Key, action)):
                        self.keyboard.release(Key[action])
                    else:
                        pyautogui.keyUp(action)
                elif (type == 'hold'):
                    self.hold_time = 0
        
        self.active_buttons = current_buttons