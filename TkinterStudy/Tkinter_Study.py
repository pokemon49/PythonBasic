#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'学习程序应用界面'
from tkinter import *
__author__ = '林金行'

def buttonClicked():
    print("Button is Clicked")

app= Frame()
#-----------------------------------------------
frame0 = Frame(app.master)
optionChoices = ['Green','Red','Yellow']
optionValue = StringVar()
option = OptionMenu(frame0,optionValue,*optionChoices)
optionValue.set("Green")
textInput = Text(frame0,width=25,height=0)
radio = Radiobutton(frame0,text="Radio")

option.pack(fill=X,padx=10,pady=4,side=LEFT,ipadx=10)
textInput.pack(fill=X,padx=10,pady=4,side=LEFT,ipadx=10)
radio.pack(fill=X,padx=10,pady=4,side=LEFT,ipadx=10)
frame0.pack(fill=BOTH,side=LEFT,expand=NO,anchor= CENTER)
#------------------------------------------------
frame1 = Frame(app.master)
checkvalue = BooleanVar()
label = Label(frame1,text = 'Label',width = 10,bg='gray',fg='black')
labe2 = Label(frame1,text = 'Labe2',width = 20,bg='white',fg='black')
button = Button(frame1,text = 'Button',width = 10,command = buttonClicked())
entry = Entry(frame1,width = 25)
check = Checkbutton(frame1,variable= checkvalue,onvalue=True,offvalue=False)
checkLabel = Label(frame1,text = 'Check',fg = 'black',)
checkvalue.set(True)

label.pack(fill=X, padx=0, pady=0, side=LEFT, ipadx=0)
#labe2.pack(fill=X, padx=10, pady=4, side=LEFT, ipadx=10)
#entry.pack(fill=X, padx=10, pady=4, side=LEFT, ipadx=10)
#button.pack(fill=X, padx=15, pady=20, side=LEFT, ipadx=10)
check.pack(fill=X, side=LEFT)
checkLabel.pack(fill=X, padx=0, pady=4, side=LEFT, ipadx=0)
frame1.pack(side=TOP, fill=BOTH, expand=NO, anchor=CENTER)
#------------------------------------------------
app.master.geometry('640x480')
app.master.resizable()
app.master.title("Windows")
app.master.mainloop()