#!/usr/bin/env python

import argparse
import pygame as pg
import pynput
import tkinter as tk
from tkinter import ttk

from pynput.keyboard import Controller

PROGNAME = "Handbell Manager for Mac"
VERSION = "0.1.1-SNAPSHOT"

scale = 2048

axisOptions = [ "X", "Y", "Z" ]

def convertAxis(a):
    return axisOptions.index(a)

name = [ "Right", "Left" ] # The name of the bell
key = [ 'j', 'f' ] # Bell 0 is right, so press 'j'; bell 1 is left, so press 'f'

# Default values - after initialisation, the values are taken from the Tkinter variables in the GUI
controller = [ 0, 1 ] # Which controller corresponds to the bell?
axis = [ "Z", "Z" ] # Which input axis to use
hand_strike = [ 100, 100 ] # Handstroke strike point
back_strike = [ -600, -600 ] # Backstroke strike point

numJoysticks = 0
js = [ ]  # Joystick objects
controllerVar = []
inputVar = []
handstrokeVar = []
axisVar = []
handstrokeCountVar = []
keyboard = []
backstrokeVar = []
backstrokeCountVar = []
root = None

# This one is the actual store of the handstroke/backstroke state
handstroke = [ True, True ] # Is the next stroke for this bell a handstroke?

debounce = 200  # Don't ring more often than this
next_ring = [ 0, 0 ]   # The time after which it is possible to ring again

keyboard = Controller()
pg.init()
print("Monitoring handbell controller\n")
numJoysticks = pg.joystick.get_count()
print("Joysticks found: ", numJoysticks)
js = [ ]
for n in range(numJoysticks):
    js.append(pg.joystick.Joystick(n))
    js[n].init()

controllerOptions = [ ]
for n in range(numJoysticks):
    controllerOptions.append(str(n))

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False 

def update():
    pg.event.get()
    for n in range(numJoysticks):
        thisController = int(controllerVar[n].get())
        thisAxis = convertAxis(axisVar[n].get())
        axisValue = js[thisController].get_axis(thisAxis) * scale
        inputVar[n].set("{0:>5}".format(100*round(axisValue / 100)))
        if axisValue > int(handstrokeVar[n].get()) and handstroke[n] and pg.time.get_ticks() > next_ring[n]:
            #print("Handstroke for bell %s at %s\n" % (n,int(handstrokeVar[n].get())))
            handstrokeCountVar[n].set(handstrokeCountVar[n].get()+1)
            keyboard.press(key[n])
            pg.time.wait(5)
            keyboard.release(key[n])
            next_ring[n] = pg.time.get_ticks() + debounce
            handstroke[n] = False
        if axisValue < int(backstrokeVar[n].get()) and not handstroke[n] and pg.time.get_ticks() > next_ring[n]:
            #print("Backstroke for bell %s at %s\n" % (n,int(backstrokeVar[n].get())))
            backstrokeCountVar[n].set(backstrokeCountVar[n].get()+1)
            keyboard.press(key[n])
            pg.time.wait(5)
            keyboard.release(key[n])
            next_ring[n] = pg.time.get_ticks() + debounce
            handstroke[n] = True
    root.after(5,update)

def runHandbellManager():
    keyboard = Controller()
    pg.init()
    #print("Monitoring handbell controller\n")
    numJoysticks = min(pg.joystick.get_count(),2)
    #print("Joysticks found: ", numJoysticks)
    for n in range(numJoysticks):
        js.append(pg.joystick.Joystick(n))
        js[n].init()

    controllerOptions = [ ]
    for n in range(numJoysticks):
        controllerOptions.append(str(n))

    root = tk.Tk()
    root.title("Handbell Manager Mac")
    validate = root.register(isInt)
    root.after(5,update)

    bellRowTitle = tk.Label(root,text="Bell",width=10,anchor="w")
    bellRowTitle.grid(row=0,column=0)

    bellColTitle = [ ]
    for n in range(numJoysticks):
        bellColTitle.append(tk.Label(root,text=name[n],width=6,anchor="e"))
        bellColTitle[n].grid(row=0,column=2-n)

    controllerRowTitle = tk.Label(root,text="Controller",width=10,anchor="w")
    controllerRowTitle.grid(row=1,column=0)

    controllerVar = [ ]
    controllerField = [ ]
    for n in range(numJoysticks):
        controllerVar.append(tk.StringVar())
        controllerVar[n].set(controller[n])
        controllerField.append(ttk.Combobox(root,width=2,textvariable=controllerVar[n],values=controllerOptions,state="readonly"))
        controllerField[n].grid(row=1,column=2-n)

    axisRowTitle = tk.Label(root,text="Axis",width=10,anchor="w")
    axisRowTitle.grid(row=2,column=0)

    axisVar = [ ]
    axisField = [ ]
    for n in range(numJoysticks):
        axisVar.append(tk.StringVar())
        axisVar[n].set(axis[n])
        axisField.append(ttk.Combobox(root,width=2,textvariable=axisVar[n],values=["X","Y","Z"],state="readonly"))
        axisField[n].grid(row=2,column=2-n)

    handstrokeRowTitle = tk.Label(root,text="Handstroke",width=10,anchor="w")
    handstrokeRowTitle.grid(row=3,column=0)

    handstrokeVar = [ ]
    handstrokeField = [ ]
    for n in range(numJoysticks):
        handstrokeVar.append(tk.StringVar())
        handstrokeVar[n].set(hand_strike[n])
        handstrokeField.append(tk.Entry(root,textvariable=handstrokeVar[n],width=6,justify="right",validate="key",validatecommand=(validate,'%P')))
        handstrokeField[n].grid(row=3,column=2-n)

    backstrokeRowTitle = tk.Label(root,text="Backstroke",width=10,anchor="w")
    backstrokeRowTitle.grid(row=4,column=0)

    backstrokeVar = [ ]
    backstrokeField = [ ]
    for n in range(numJoysticks):
        backstrokeVar.append(tk.StringVar())
        backstrokeVar[n].set(back_strike[n])
        backstrokeField.append(tk.Entry(root,textvariable=backstrokeVar[n],width=6,justify="right",validate="key",validatecommand=(validate,'%P')))
        backstrokeField[n].grid(row=4,column=2-n)

    inputRowTitle = tk.Label(root,text="Input",width=10,anchor="w")
    inputRowTitle.grid(row=5,column=0)

    inputVar = [ ]
    inputField = [ ]
    for n in range(numJoysticks):
        inputVar.append(tk.StringVar())
        inputField.append(tk.Label(root,textvariable=inputVar[n],width=6,anchor="e"))
        inputField[n].grid(row=5,column=2-n)

    handstrokeCountRowTitle = tk.Label(root,text="#Handstrokes",width=10,anchor="w")
    handstrokeCountRowTitle.grid(row=6,column=0)

    handstrokeCountVar = [ ]
    handstrokeCountField = [ ]
    for n in range(numJoysticks):
        handstrokeCountVar.append(tk.IntVar())
        handstrokeCountVar[n].set(0)
        handstrokeCountField.append(tk.Label(root,textvariable=handstrokeCountVar[n],width=6,justify="right"))
        handstrokeCountField[n].grid(row=6,column=2-n)

    backstrokeCountRowTitle = tk.Label(root,text="#Backstrokes",width=10,anchor="w")
    backstrokeCountRowTitle.grid(row=7,column=0)

    backstrokeCountVar = [ ]
    backstrokeCountField = [ ]
    for n in range(numJoysticks):
        backstrokeCountVar.append(tk.IntVar())
        backstrokeCountVar[n].set(0)
        backstrokeCountField.append(tk.Label(root,textvariable=backstrokeCountVar[n],width=6,justify="right"))
        backstrokeCountField[n].grid(row=7,column=2-n)

    tk.mainloop()

def displayVersionInfo():
    print("Handbell Manager for Mac " + VERSION + "\n")

# Main script

parser = argparse.ArgumentParser(description="HandbellManagerMac arguments")
parser.add_argument("--version", action='version', version=f'{PROGNAME} {VERSION}')
args = parser.parse_args()

runHandbellManager()
