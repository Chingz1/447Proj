#from tkinter import *
import os
import tkinter as tk
import subprocess as sub
import sys
global G_out
PIPE ='|'

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Welcome to the Schedule Generator!")
       label.pack(side="top", fill="both", expand=True)
def generate():
    #os.system('python3 schedule2.py ClassRoom.xlsx output.csv')
    global G_out
    if not path.exists('ClassRoom.xlsx') or not path.exists('output.csv'):
        raise ImportError('Please enter a classroom file (.xlsx) followed by an output file in the command line.')
        
    output= sub.run(['python3','schedule2.py','ClassRoom.xlsx','output.csv'], check=True,capture_output=True).stdout
    output= str(output)[2:]
    G_out = output.split('\\n')
    #x = sub.check_output(['python3','schedule2.py','ClassRoom.xlsx','output.csv'])
    #sys.stdout = Std_redirector(text)
    #p = sub.Popen('python3 schedule2.py ClassRoom.xlsx output.csv',stdout=sub.PIPE,stderr=sub.PIPE)
    #output, errors = p.communicate()
    
def view_schedule():
    global G_out
    master = tk.Tk()
    scrollbar = tk.Scrollbar(master)
    scrollbar.pack(side="right", fill = tk.Y, expand=False)
    listbox = tk.Listbox(master, yscrollcommand=scrollbar.set)
    for i in range(len(G_out)):
        listbox.insert(tk.END, str(G_out[i]))
        #listbox.insert(tk.END, '\n')
    listbox.pack(side="left", fill=tk.BOTH,expand=True)

    scrollbar.config(command=listbox.yview_scroll)
    
    temp = tk.Button( text="test")
    outputfile = open("output.csv")
    
    outputfile.close()
    master.mainloop()

class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Show schedule here")
       label.pack(side="top", fill="both", expand=True)

class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Show statistics here")
       label.pack(side="top", fill="both", expand=True)
        
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Generate Schedule", command=generate)
        b2 = tk.Button(buttonframe, text="View Schedule", command=view_schedule)
        b3 = tk.Button(buttonframe, text="View Statistics", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both" ,expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
'''

def generate():
    os.system('python3 schedule2.py ClassRoom.xlsx output.csv')
    
root = Tk()
frame = Frame(root)
frame.pack()

root.geometry("500x100")

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

 

generatebutton = Button(frame, text = "Generate Schedule", fg = "black", command=generate)
generatebutton.pack()# side = LEFT)

 

viewbutton = Button(frame, text = "View Schedule", fg = "black")
viewbutton.pack()# side = RIGHT )


 

root.mainloop()
'''
