import tkinter
import time
import Config
import darkdetect

class Message():
    MESSAGES_ACTIVE = True
    
    def __init__(self):
        settings = Config.get_settings()
        
        if (settings['showMessages'] != None and
            settings['showMessages'] == False):
            self.MESSAGES_ACTIVE = False
        
    def show(self, message: str, duration: float, fade_out: bool = True):
        if (self.MESSAGES_ACTIVE == False):
            return
        self.duration = duration
        self.win = tkinter.Tk()
        self.win.attributes('-alpha', 0)
        self.win.attributes('-topmost',True)
        
        # style
        background = 'black'
        foreground = 'white'
        try:
            if darkdetect.isDark() == False:
                background = 'white'
                foreground = 'black'
        except:
            pass
        
        text = tkinter.Text(
            self.win,
            height=1,
            width=len(message),
            background=background,
            foreground=foreground,
            borderwidth=0,
            font='Consolas 20',
            padx=100,
            pady=10)
        self.win.overrideredirect(True)
        
        # center
        self.win.update_idletasks()
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        size = tuple(int(_) for _ in self.win.geometry().split('+')[0].split('x'))
        x = screen_width*.5 - size[0]*.5
        y = screen_height*.8 - size[1]*.5
        self.win.geometry("+%d+%d" % (x, y))
        
        text.pack()
        text.insert(tkinter.END, message)
        
        self.win.attributes('-alpha', .2)
        self.win.update_idletasks()
        
        if (fade_out == True):
            self.end = False
            self.exec_time = time.time()
            self.win.after(
                int(duration*1000*.8),
                lambda:self.__fade_out()
            )
        else:
            self.win.after(
                int(duration*1000),
                lambda:self.__end()
            )
        
        self.win.mainloop()
    
    def __fade_out(self):
        self.win.after(
            int(self.duration*1000*.2),
            lambda:self.__fade_out()
        )
        
        if (self.end == True):
            self.__end()
        else:
            self.win.attributes('-alpha', .1)
            self.win.update_idletasks()
            self.end = True
    
    def __end(self):
        self.win.destroy()