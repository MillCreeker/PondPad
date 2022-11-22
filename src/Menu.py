from tkinter import *
import os
import darkdetect
import Notification
import Config
from GamePad import GamePad

class MenuExit(Exception):
    pass

class Menu():
    background_color = 'black'
    foreground_color = 'white'
    background_color_alt = 'white'
    foreground_color_alt = 'black'
    
    is_select_pressed = False
    
    def __init__(self):
        try:
            if darkdetect.isDark() == False:
                self.background_color = 'white'
                self.foreground_color = 'black'
                self.background_color_alt = 'black'
                self.foreground_color_alt = 'white'
        except:
            pass
        
        self.gp = GamePad()
    
    def show(self):
        settings = Config.get_settings()
        is_frame_less = False
        if (settings['menuGrabbable'] == False):
            is_frame_less = True
        
        # general
        self.win = Tk()
        self.win.attributes('-alpha', 0)
        self.win.attributes('-topmost', True)
        self.win.title('Quit?')
        self.win.overrideredirect(is_frame_less)
        self.win.configure(background=self.background_color)
        
        font = 'Consolas 20'
        
        self.buttons = []
        self.focused_button = None
        
        # cancel button        
        self.cancel_btn = Button(
            self.win,
            text='Cancel',
            command=self.__exit_menu,
            font=font,
            background=self.background_color,
            foreground=self.foreground_color,
            border=0
        )
        self.cancel_btn.grid(row=0, column=1, padx= 20, pady= 10)
        self.buttons.append(self.cancel_btn)
        
        # exit button
        self.exit_btn = Button(
            self.win,
            text='Exit',
            command=self.__end_program,
            font=font,
            background=self.background_color,
            foreground=self.foreground_color,
            border=0
        )
        self.exit_btn.grid(row=0, column=2, padx= 20, pady= 10)
        self.buttons.append(self.exit_btn)
        
        # center
        self.win.update_idletasks()
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        size = tuple(int(_) for _ in self.win.geometry().split('+')[0].split('x'))
        x = screen_width*.5 - size[0]*.5
        y = screen_height*.5 - size[1]*.5
        self.win.geometry("+%d+%d" % (x, y))
        
        if (is_frame_less == True):
            self.win.attributes('-alpha', .6)
        else:
            self.win.attributes('-alpha', 1)
        
        self.__focus_button(self.cancel_btn)
        self.win.update_idletasks()
        
        try:
            def show_error(self, *args):
                raise MenuExit
            Tk.report_callback_exception = show_error
            
            self.win.after(10, lambda:self.__get_input())
            self.win.mainloop()
            
            # self.__exit_menu(self)
        except:
            self.win.withdraw()
            raise MenuExit
    
    def __exit_menu(self):
        raise MenuExit
    
    def __end_program(self):
        Notification.show(
            'Pond Pad has stopped',
            ' '
        )
        os._exit(0)
    
    def __focus_button(self, btn: Button):
        for button in self.buttons:
            if (button != btn):
                button.configure(
                    background = self.background_color,
                    foreground = self.foreground_color
                )
        
        btn.configure(
            background = self.background_color_alt,
            foreground = self.foreground_color_alt
        )
        self.win.update_idletasks()
        self.focused_button = btn
    
    def __get_input(self):
        input = self.gp.read()
        for button in dir(input):
            value = getattr(input, button)
            if (value == 0):
                if (button == 'Select' and
                    self.is_select_pressed == True):
                    self.is_select_pressed = False
                    self.__exit_menu()
                continue
            
            if (button == 'DPadLeft' and
                self.focused_button == self.exit_btn):
                self.__focus_button(self.cancel_btn)
            elif (button == 'DPadRight' and
                self.focused_button == self.cancel_btn):
                self.__focus_button(self.exit_btn)
            elif (button == 'Select'):
                self.is_select_pressed = True
            elif (button == 'B'):
                self.__exit_menu()
            elif (button == 'A'):
                if (self.focused_button == self.cancel_btn):
                    self.__exit_menu()
                elif (self.focused_button == self.exit_btn):
                    self.__end_program()
            
            self.win.after(10, lambda:self.__get_input())
    
    def show(self):
        self.win.deiconify()