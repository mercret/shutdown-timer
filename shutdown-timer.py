from tkinter import *
import datetime
import os
import platform
import time

SHUTDOWN_COMMANDS = {'Windows': 'shutdown /s', 'Linux': 'shutdown'}


class ShutdownTimer(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Shutdown Timer')
        self.resizable(False, False)

        self.started = False
        self.target = datetime.datetime.now()

        self.countdownVar = StringVar(value='00:00:00')
        self.hour = IntVar(value=0)
        self.minute = IntVar(value=0)

        Label(self, text='Shutdown Time').grid(row=0, column=0, padx=5, pady=5)
        self.hourSpinbox = Spinbox(self, from_=0, to=23, width=2, textvariable=self.hour)
        self.hourSpinbox.grid(row=0, column=1, padx=5, pady=5)
        Label(self, text=':').grid(row=0, column=2)
        self.minuteSpinbox = Spinbox(self, from_=0, to=59, width=2, textvariable=self.minute)
        self.minuteSpinbox.grid(row=0, column=3, padx=5, pady=5)

        self.countdownLabel = Label(self, textvariable=self.countdownVar).grid(
            row=1, column=0, padx=5, pady=5)
        self.startButton = Button(self, text='Start', command=self.start)
        self.startButton.grid(
            row=1, column=1, columnspan=3, padx=5, pady=5)

        self.command = SHUTDOWN_COMMANDS[platform.system()]

    def countdown(self):
        if self.started:
            delta = self.target - datetime.datetime.now()
            if delta < datetime.timedelta(0):
                # os.system(self.command)
            else:
                self.countdownVar.set('{:02}:{:02}:{:02}'.format(delta.seconds//3600, delta.seconds//60%60, delta.seconds%60))
                self.after(1000, self.countdown)

    def start(self):
        if self.started:
            self.started = False
            self.startButton['text'] = 'Start'
            self.hourSpinbox['state'] = 'normal'
            self.minuteSpinbox['state'] = 'normal'
        else:
            self.started = True
            self.startButton['text'] = 'Stop'
            self.hourSpinbox['state'] = 'disabled'
            self.minuteSpinbox['state'] = 'disabled'


            now = datetime.datetime.now()
            target_time = datetime.time(self.hour.get(), self.minute.get())
            if target_time > now.time():
                self.target = datetime.datetime.combine(datetime.datetime.today(), target_time)
            else:
                self.target = datetime.datetime.combine(
                    datetime.datetime.today() + datetime.timedelta(days=1), target_time)
            self.countdown()


root = ShutdownTimer()
root.mainloop()
