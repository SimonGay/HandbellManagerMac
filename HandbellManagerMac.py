#!/usr/bin/env python

import time
import pygame as pg
import pynput
import tkinter as tk
from tkinter import ttk
import os.path
import pickle

from pynput.keyboard import Controller

# General initialisation

scale = 2048
axisOptions = [ "X", "Y", "Z" ]
keyboard = Controller()
numJoysticks = 0
js = [ ] # The joysticks
controllerOptions = [ ] # The joystick numbers
name = [ ] # The names of the bells
key = [ ] # Which keypress to generate for each bell
controller = [ ] # Which controller corresponds to the bell?
axis = [ ] # Which input axis to use for each bell
leftButton = [ ] # Which keypress to generate for the left button
rightButton = [ ] # Which keypress to generate for the right button
hand_strike = [ ] # Handstroke strike point for each bell
back_strike = [ ] # Backstroke strike point for each bell
handstroke = [ ] # Is the next stroke for this bell a handstroke?
next_ring = [ ]   # The time after which it is possible to ring again
next_press = [ ] # The time after which it is possible to press a button again
debounce = 600  # Don't ring more often than this
bellColTitle = [ ] # The labels at the tops of the columns for the bells

defaultHandStrike = 100
defaultBackStrike = -600

# The next set of variables are for each row of the grid. A Tkinter variable and a GUI field for each column.
controllerVar = [ ]
controllerField = [ ]
axisVar = [ ]
axisField = [ ]
keyVar =[ ]
keyField = [ ]
buttonLVar = [ ]
buttonLField = [ ]
buttonRVar = [ ]
buttonRField = [ ]
handstrokeVar = [ ]
handstrokeField = [ ]
backstrokeVar = [ ]
backstrokeField = [ ]
inputVar = [ ]
inputField = [ ]
handstrokeCountVar = [ ]
handstrokeCountField = [ ]
backstrokeCountVar = [ ]
backstrokeCountField = [ ]


def reset():
    global bellColTitle
    global name
    global controllerOptions
    global controllerVar
    global controllerField
    global axisVar
    global axisField
    global keyVar
    global keyField
    global buttonLVar
    global buttonLField
    global buttonRVar
    global buttonRField
    global handstrokeVar
    global handstrokeField
    global backstrokeVar
    global backstrokeField
    global inputVar
    global inputField
    global handstrokeCountVar
    global handstrokeCountField
    global backstrokeCountVar
    global backstrokeCountField
    bellColTitle = [ ]
    name = [ ]
    controllerOptions = [ ]
    controllerVar = [ ]
    controllerField = [ ]
    axisVar = [ ]
    axisField = [ ]
    keyVar = [ ]
    keyField = [ ]
    buttonLVar = [ ]
    buttonLField = [ ]
    buttonRVar = [ ]
    buttonRField = [ ]
    handstrokeVar = [ ]
    handstrokeField = [ ]
    backstrokeVar = [ ]
    backstrokeField = [ ]
    inputVar = [ ]
    inputField = [ ]
    handstrokeCountVar = [ ]
    handstrokeCountField = [ ]
    backstrokeCountVar = [ ]
    backstrokeCountField = [ ]

def removeWidgets():
    for x in bellColTitle:
        x.grid_remove()
    for x in controllerField:
        x.grid_remove()
    for x in axisField:
        x.grid_remove()
    for x in keyField:
        x.grid_remove()
    for x in buttonLField:
        x.grid_remove()
    for x in buttonRField:
        x.grid_remove()
    for x in handstrokeField:
        x.grid_remove()
    for x in backstrokeField:
        x.grid_remove()
    for x in inputField:
        x.grid_remove()
    for x in handstrokeCountField:
        x.grid_remove()
    for x in backstrokeCountField:
        x.grid_remove()

def reDetectBells():
    pg.quit()
    detectBells()

def detectBells():
    global numJoysticks
    global hand_strike
    global back_strike
    removeWidgets()
    reset()
    pg.init()
    numJoysticks = pg.joystick.get_count()
    print("Bells found: ", numJoysticks)
    numJoysticks = max(numJoysticks,2)
    print("Using ", numJoysticks, " bells.")
    for n in range(numJoysticks):
        js.append(pg.joystick.Joystick(n))
        js[n].init()     
    # Default and initial values
    if numJoysticks == 1:
        key.append("j")
        name.append("Right")
        leftButton.append("l")
        rightButton.append("g")
    elif numJoysticks == 2:
        key.append("j")
        key.append("f")
        name.append("Right")
        name.append("Left")
        leftButton.append("l")
        rightButton.append("g")
        leftButton.append("b")
        rightButton.append("n")
    #print("Names: ", name)
    for n in range(numJoysticks):
        controllerOptions.append(n) # The physical bell number
        axis.append("Z") # The input axis
        hand_strike.append(defaultHandStrike) # The handstroke strike point
        back_strike.append(defaultBackStrike) # The backstroke strike point
        handstroke.append(True) # Start with a handstroke
        next_ring.append(0) # Start the debounce timer from zero
        next_press.append(0)
    # If there are files with saved strike settings, load them
    if os.path.isfile("hand.pkl"):
        handfile = open("hand.pkl","rb")
        hand_strike = pickle.load(handfile)
        handfile.close()
        if len(hand_strike) < numJoysticks:
            for i in range(numJoysticks-len(hand_strike)):
                hand_strike.append(defaultHandStrike)
    if os.path.isfile("back.pkl"):
        backfile = open("back.pkl","rb")
        back_strike = pickle.load(backfile)
        backfile.close()
        if len(back_strike) < numJoysticks:
            for i in range(numJoysticks-len(back_strike)):
                back_strike.append(defaultBackStrike)
    # If there are some bells, set up their names
    if numJoysticks > 0:
        for n in range(numJoysticks):
            bellColTitle.append(tk.Label(root,text=name[n],width=6))
            bellColTitle[n].grid(row=0,column=numJoysticks-n)
    else: # Otherwise, display a message
        bellColTitle.append(tk.Label(root,text="No bells detected ",fg="red",anchor="e"))
        bellColTitle[0].grid(row=0,column=1)
    # Set up the columns in the grid, one for each bell
    for n in range(numJoysticks):
        # The physical bell number for each logical bell
        controllerVar.append(tk.StringVar())
        controllerVar[n].set(controllerOptions[n])
        controllerField.append(ttk.Combobox(root,width=2,textvariable=controllerVar[n],values=controllerOptions,state="readonly"))
        controllerField[n].grid(row=1,column=numJoysticks-n)
        # The input axis
        axisVar.append(tk.StringVar())
        axisVar[n].set(axis[n])
        axisField.append(ttk.Combobox(root,width=2,textvariable=axisVar[n],values=axisOptions,state="readonly"))
        axisField[n].grid(row=2,column=numJoysticks-n)
        # The keypress to generate
        keyVar.append(tk.StringVar())
        keyVar[n].set(key[n])
        if numJoysticks < 3:
            keyField.append(tk.Entry(root,textvariable=keyVar[n],width=6,justify="right"))
        else:
            keyField.append(ttk.Combobox(root,width=2,textvariable=keyVar[n],values=keyOptions,state="readonly"))
        keyField[n].grid(row=3,column=numJoysticks-n)
        # The keypress for the left button
        buttonLVar.append(tk.StringVar())
        buttonLVar[n].set(leftButton[n])
        buttonLField.append(tk.Entry(root,textvariable=buttonLVar[n],width=6,justify="right"))
        buttonLField[n].grid(row=4,column=numJoysticks-n)
        # The keypress for the right button
        buttonRVar.append(tk.StringVar())
        buttonRVar[n].set(rightButton[n])
        buttonRField.append(tk.Entry(root,textvariable=buttonRVar[n],width=6,justify="right"))
        buttonRField[n].grid(row=5,column=numJoysticks-n)
        # The handstroke strike point
        handstrokeVar.append(tk.StringVar())
        handstrokeVar[n].set(hand_strike[n])
        handstrokeField.append(tk.Entry(root,textvariable=handstrokeVar[n],width=6,justify="right",validate="key",validatecommand=(validate,'%P')))
        handstrokeField[n].grid(row=6,column=numJoysticks-n)
        # The backstroke strike point
        backstrokeVar.append(tk.StringVar())
        backstrokeVar[n].set(back_strike[n])
        backstrokeField.append(tk.Entry(root,textvariable=backstrokeVar[n],width=6,justify="right",validate="key",validatecommand=(validate,'%P')))
        backstrokeField[n].grid(row=7,column=numJoysticks-n)
        # The display of the current input value
        inputVar.append(tk.StringVar())
        inputField.append(tk.Label(root,textvariable=inputVar[n],width=6,bg="#caf7c8",anchor="e"))
        inputField[n].grid(row=8,column=numJoysticks-n)
        # Counting handstrokes
        handstrokeCountVar.append(tk.IntVar())
        handstrokeCountVar[n].set(0)
        handstrokeCountField.append(tk.Label(root,textvariable=handstrokeCountVar[n],width=6,justify="right"))
        handstrokeCountField[n].grid(row=9,column=numJoysticks-n)
        # Counting backstrokes
        backstrokeCountVar.append(tk.IntVar())
        backstrokeCountVar[n].set(0)
        backstrokeCountField.append(tk.Label(root,textvariable=backstrokeCountVar[n],width=6,justify="right"))
        backstrokeCountField[n].grid(row=10,column=numJoysticks-n)

def restoreDefaults():
    global hand_strike
    global back_strike
    hand_strike = [ ]
    back_strike = [ ]
    for n in range(numJoysticks):
        hand_strike.append(defaultHandStrike)
        handstrokeVar[n].set(hand_strike[n])
        back_strike.append(defaultBackStrike) 
        backstrokeVar[n].set(back_strike[n])
        update()
    
def start():
    # Just take the focus away from any text field that the user has been typing into
    bellRowTitle.focus()

def terminate():
    # Save the strike settings and exit
    global hand_strike
    global back_strike
    hand_strike = [ ]
    for n in range(numJoysticks):
        hand_strike.append(handstrokeVar[n].get())
    handfile = open("hand.pkl","wb")
    pickle.dump(hand_strike,handfile)
    #print("Writing ",hand_strike)
    handfile.close()
    back_strike = [ ]
    for n in range(numJoysticks):
        back_strike.append(backstrokeVar[n].get())
    backfile = open("back.pkl","wb")
    pickle.dump(back_strike,backfile)
    #print("Writing ",back_strike)
    backfile.close()
    root.destroy()

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def convertAxis(a):
    return axisOptions.index(a)

def update():
    pg.event.get()
    for n in range(numJoysticks):
        thisController = int(controllerVar[n].get())
        thisAxis = convertAxis(axisVar[n].get())
        axisValue = js[thisController].get_axis(thisAxis) * scale
        inputVar[n].set("{0:>5}".format(100*round(axisValue / 100)))
        leftButtonValue = js[thisController].get_button(0)
        rightButtonValue = js[thisController].get_button(1)
        if axisValue > int(handstrokeVar[n].get()) and handstroke[n] and pg.time.get_ticks() > next_ring[n]:
            #print("Handstroke for bell %s at %s\n" % (n,int(handstrokeVar[n].get())))
            handstrokeCountVar[n].set(handstrokeCountVar[n].get()+1)
            keyboard.press(keyVar[n].get())
            pg.time.wait(5)
            keyboard.release(keyVar[n].get())
            next_ring[n] = pg.time.get_ticks() + debounce
            handstroke[n] = False
        if axisValue < int(backstrokeVar[n].get()) and not handstroke[n] and pg.time.get_ticks() > next_ring[n]:
            #print("Backstroke for bell %s at %s\n" % (n,int(backstrokeVar[n].get())))
            backstrokeCountVar[n].set(backstrokeCountVar[n].get()+1)
            keyboard.press(keyVar[n].get())
            pg.time.wait(5)
            keyboard.release(keyVar[n].get())
            next_ring[n] = pg.time.get_ticks() + debounce
            handstroke[n] = True
        if leftButtonValue:
            buttonLField[n]["bg"] = "#caf7c8"
        else:
            buttonLField[n]["bg"] = "#ffffff"
        if rightButtonValue:
            buttonRField[n]["bg"] = "#caf7c8"
        else:
            buttonRField[n]["bg"] = "#ffffff"
        if leftButtonValue and pg.time.get_ticks() > next_press[n]:
            keyboard.press(leftButton[n])
            pg.time.wait(5)
            keyboard.release(leftButton[n])
            next_press[n] = pg.time.get_ticks() + debounce
        if rightButtonValue and pg.time.get_ticks() > next_press[n]:
            keyboard.press(rightButton[n])
            pg.time.wait(5)
            keyboard.release(rightButton[n])
            next_press[n] = pg.time.get_ticks() + debounce
    root.after(5,update)

# This is where we start constructing the GUI

root = tk.Tk()
root.title("Handbell Manager Mac")
validate = root.register(isInt)
root.after(5,update)

bellRowTitle = tk.Label(root,text=" Bell ",width=13,borderwidth=1,relief="ridge",anchor="w")
bellRowTitle.grid(row=0,column=0)

controllerRowTitle = tk.Label(root,text=" Controller ",width=13,borderwidth=1,relief="ridge",anchor="w")
controllerRowTitle.grid(row=1,column=0)

axisRowTitle = tk.Label(root,text=" Axis ",width=13,borderwidth=1,relief="ridge",anchor="w")
axisRowTitle.grid(row=2,column=0)

keyRowTitle = tk.Label(root,text=" Key ",width=13,borderwidth=1,relief="ridge",anchor="w")
keyRowTitle.grid(row=3,column=0)

leftRowTitle = tk.Label(root,text=" Left Button ",width=13,borderwidth=1,relief="ridge",anchor="w")
leftRowTitle.grid(row=4,column=0)

rightRowTitle = tk.Label(root,text=" Right Button ",width=13,borderwidth=1,relief="ridge",anchor="w")
rightRowTitle.grid(row=5,column=0)

handstrokeRowTitle = tk.Label(root,text=" Handstroke ",width=13,borderwidth=1,relief="ridge",anchor="w")
handstrokeRowTitle.grid(row=6,column=0)

backstrokeRowTitle = tk.Label(root,text=" Backstroke ",width=13,borderwidth=1,relief="ridge",anchor="w")
backstrokeRowTitle.grid(row=7,column=0)

inputRowTitle = tk.Label(root,text=" Input ",width=13,borderwidth=1,relief="ridge",anchor="w")
inputRowTitle.grid(row=8,column=0)

handstrokeCountRowTitle = tk.Label(root,text=" #Handstrokes ",width=13,borderwidth=1,relief="ridge",anchor="w")
handstrokeCountRowTitle.grid(row=9,column=0)

backstrokeCountRowTitle = tk.Label(root,text=" #Backstrokes ",width=13,borderwidth=1,relief="ridge",anchor="w")
backstrokeCountRowTitle.grid(row=10,column=0)

emptyRowTitle = tk.Label(root,text=" ")
emptyRowTitle.grid(row=11,column=0)

detectBellsButton = tk.Button(root,text="Detect bells",width=13,borderwidth=1,relief="ridge",command=reDetectBells)
detectBellsButton.grid(row=12,column=0)

restoreDefaultsButton = tk.Button(root,text="Restore defaults",width=13,borderwidth=1,relief="ridge",command=restoreDefaults)
restoreDefaultsButton.grid(row=13,column=0)

startButton = tk.Button(root,text="Start",width=13,borderwidth=1,relief="ridge",command=start)
startButton.grid(row=14,column=0)

quitButton = tk.Button(root,text="Quit",width=13,borderwidth=1,relief="ridge",command=terminate)
quitButton.grid(row=14,column=1)

detectBells()

tk.mainloop()

