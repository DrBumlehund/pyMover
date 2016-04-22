#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

from tkinter import *
from tkinter import messagebox
import os
import pyMover

root = Tk()
root.title('pyMover')

top = Frame(root)
top.pack(side=TOP)

bottom = Frame(root)
bottom.pack(side=BOTTOM)

L1 = Label(top, text='Instruction set:')
L1.pack(side=LEFT)

E1 = Entry(top, bd=0.5)
E1.pack(side=RIGHT)

result = StringVar()
L2 = Label(bottom, textvariable=result)

result.set('')


def button_click():
    instruction_set = E1.get()
    if len(instruction_set) > 0:
        if os.path.isfile(instruction_set) and str(instruction_set).endswith('.txt'):
            result.set(pyMover.run(instruction_set))
        else:
            messagebox.showinfo('Whoops', 'Invalid path to instruction set.')
    else:
        messagebox.showinfo('Whoops', 'You need to set a path for the instruction set.')


B = Button(bottom, text='Run cleaner', command=button_click)
B.pack(side=TOP)
L2.pack(side=BOTTOM)

root.mainloop()
