# from tkinter import *
import os
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import sys
import pandas as pd

global G_out
global inFile
global outFile
PIPE = '|'
#colors
GOLD='#ffbf00'
BACKGROUND='#FFF8F4'


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs, bg='blue')

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Welcome to the Schedule Generator!")
        label.pack(side='bottom', anchor=tk.S, fill="both", expand=True)


def on_closing():
    if messagebox.askokcancel("Quit", "Hold up! Closing this window will quit the program. Do you want to quit?"):
        root.destroy()
        sys.exit()


def generate():
    runthis = 'python3 schedule2.py ' + inFile + ' ' + outFile
    os.system(runthis)


def view_schedule():
    master = tk.Tk()
    scrollbar = tk.Scrollbar(master)
    master.title('View Schedule')
    scrollbar.pack(side="right", fill=tk.Y, expand=False)
    listbox = tk.Listbox(master, yscrollcommand=scrollbar.set,bg=BACKGROUND)
    df = pd.read_excel(outFile, sheet_name='Schedule')
    sched_list = df.values.tolist()
    print_out_list = {"Scheduled:": [], "Unscheduled:": []}

    for i in range(len(sched_list)):
        if sched_list[i][len(sched_list[i]) - 1].lower() == "scheduled":
            print_out_list["Scheduled:"].append(sched_list[i][:len(sched_list[i]) - 1])
        else:
            print_out_list["Unscheduled:"].append(sched_list[i][:len(sched_list[i]) - 1])
    for key in print_out_list.keys():
        listbox.insert(tk.END, key)
        for i in range(len(print_out_list[key])):
            listbox.insert(tk.END, str(print_out_list[key][i]))

    listbox.pack(side="left", fill=tk.BOTH, expand=True)

    scrollbar.config(command=listbox.yview_scroll)

    temp = tk.Button(text="test")
    master.mainloop()



def go(page, inF, outF):
    global inFile
    global outFile
    # do error checking for input and output files here
    inFile = str(inF.get())
    outFile = str(outF.get())
    if ".xlsx" in inF.get() and ".xlsx" in outF.get():  # Checks whether input and output files are correctly formatted
        if os.path.isfile(inFile):
            generate()
            root.deiconify()  # Unhides the root window
            page.destroy()  # Removes the toplevel window
        else:
            messagebox.showerror("File Error", "Input file could not be found.")
    else:
        messagebox.showerror("File Error", "Both the input file and output file need to be xlsx files.")


def quit_top(top, root):
    top.destroy()  # Removes the toplevel window
    root.destroy()  # Removes the hidden root window
    sys.exit()  # Ends the script
    

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.configure(bg=BACKGROUND)
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        self.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        for row_index in range(5):
            tk.Grid.rowconfigure(self, row_index, weight=1)
            for col_index in range(6):
                tk.Grid.columnconfigure(self, col_index, weight=1)
        title_label = tk.Label(self, text="Welcome to the Scheduler!", font=("Helvetica", 32),fg='white',bg='black')
        title_label.grid(row=0, column=0,columnspan=6, sticky=tk.N+tk.S+tk.E+tk.W)

        b2 = tk.Button(self, text="View Schedule", command=view_schedule, highlightthickness=0,bg=GOLD)
        b3 = tk.Button(self, text="View Statistics", highlightthickness=0,bg=GOLD)  # , command=p3.lift)
        qb = tk.Button(self, text="Quit",command=lambda:sys.exit(),highlightthickness=0,padx=5,bg=GOLD)
        contact = tk.Button(self, text= "Contact Us",command=self.contact_form,highlightthickness=0,padx=5,bg=GOLD)
        
        
        b2.grid(row=2, column=1,rowspan=2, sticky=tk.E+tk.W,padx = 10,pady=5)
        b3.grid(row=2, column=4,rowspan=2, sticky=tk.E+tk.W, padx = 10,pady=5)
        contact.grid(row=5, column=0, sticky=tk.E+tk.W, padx = 10,pady=5)
        qb.grid(row=5, column=5, sticky=tk.E+tk.W, padx = 10,pady=5)
        
    #Creates the contact us form for user comment submission
    def contact_form(self):
        self.form = tk.Toplevel(self,bg=BACKGROUND)
        self.form.title('Contact Us')
    
        tk.Grid.rowconfigure(self.form, 0, weight=1)
        tk.Grid.columnconfigure(self.form, 0, weight=1)
    
        #Create & Configure frame 
        frame=tk.Frame(self.form,bg=BACKGROUND)
        frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        for row_index in range(5):
            tk.Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(2):
                tk.Grid.columnconfigure(frame, col_index, weight=1)
                
        #creates 3 entries, name, email, comment/concern
        self.name=''
        self.email=''
        self.concern=''
        tk.Label(frame, text="Name:", bg=BACKGROUND).grid(row=0, column=0, sticky=tk.N+tk.S,padx=5)
        self.name= tk.Entry(frame)
        self.name.config(highlightthickness=0)
        self.name.grid(row=0, column=1, sticky=tk.E+tk.W)
        tk.Label(frame, text="Email:", bg=BACKGROUND).grid(row=1, column=0, sticky=tk.N+tk.S,padx=5)
        self.email = tk.Entry(frame)
        self.email.config(highlightthickness=0)
        self.email.grid(row=1, column=1, sticky=tk.E+tk.W)
        tk.Label(frame, text="Comment:", bg=BACKGROUND).grid(row=2, column=0, sticky=tk.N+tk.S,padx=5)
        self.concern = tk.Entry(frame)
        self.concern.config(highlightthickness=0)
        self.concern.grid(row=2, column=1,rowspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
        
        submit_b =  tk.Button(frame, text="Submit", command=self.comment_file, highlightthickness=0, padx=5, bg=GOLD)
        self.form.bind('<Return>', lambda e: self.comment_file())
        submit_b.grid(row=4, column=1, sticky=tk.E+tk.W)
        
    #actually writes comments to file
    def comment_file(self):

        comment = str(self.name.get())+','+str(self.email.get())+','+str(self.concern.get())+'\n'
        out_file = "user_comments.csv"
        if len(str(self.name.get()).strip())==0 or len(str(self.email.get()).strip())==0 or len(str(self.concern.get()).strip())==0:
            tk.messagebox.showwarning(title="Warning", message="Required input is missing. Comment will not be submitted.")
        else:
            if os.path.exists(out_file):
                myfile=open(out_file,'a')
                myfile.write(comment)
                myfile.close()
            else:
                myfile=open(out_file,'w')
                myfile.write('Name,Email,Comment\n')
                myfile.write(comment)
                myfile.close()
            
        #destroys contact form after writing to file
        self.form.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title('Main Menu')
    root.configure(bg=BACKGROUND)
    
    entry = tk.Toplevel(bg=BACKGROUND)
    entry.protocol("WM_DELETE_WINDOW", on_closing)
    entry.title('Start Up')
    
    tk.Grid.rowconfigure(entry, 0, weight=1)
    tk.Grid.columnconfigure(entry, 0, weight=1)
    
    #Create & Configure frame 
    frame=tk.Frame(entry,bg=BACKGROUND)
    frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
    for row_index in range(6):
        tk.Grid.rowconfigure(frame, row_index, weight=1)
        for col_index in range(5):
            tk.Grid.columnconfigure(frame, col_index, weight=1)
    
    inputFile = ''
    ouputFile = ''
    title_label = tk.Label(frame, text="Welcome to the Scheduler!", font=("Helvetica", 32),fg='white',bg='black')
    title_label.grid(row=0, column=0,columnspan=6, sticky=tk.N+tk.S+tk.E+tk.W)
    entry.bind('<Return>', lambda e: go(entry, inputFile, outputFile))
    tk.Label(frame, text="Please make sure both the input file and output file are excel workbook files (.xlsx). \n The scheduler is not designed to work with any other files", bg=BACKGROUND).grid(row=5, column=0,columnspan=6, sticky=tk.N+tk.S+tk.E+tk.W)

    tk.Label(frame, text="Input file:", bg=BACKGROUND).grid(row=3, column=0, sticky=tk.N+tk.S,padx=5)
    inputFile = tk.Entry(frame)
    inputFile.config(highlightthickness=0)
    inputFile.grid(row=3, column=1, sticky=tk.E+tk.W)
    tk.Label(frame, text="Output file:", bg=BACKGROUND).grid(row=3, column=2, sticky=tk.N+tk.S,padx=5)
    outputFile = tk.Entry(frame)
    outputFile.config(highlightthickness=0)
    outputFile.grid(row=3, column=3, sticky=tk.E+tk.W)
    
    button1 = tk.Button(frame, text="Generate", command=lambda: go(entry, inputFile, outputFile), bg=GOLD, relief=tk.RAISED)
    button1.config(highlightthickness=0)
    button2 = tk.Button(frame, text="Quit", command=lambda: quit_top(entry, root), bg=GOLD,
                        relief=tk.RAISED)  # quit button
    button2.config(highlightthickness=0)
    button1.grid(row=3, column=4, sticky=tk.E+tk.W,padx = 10,pady=5)
    button2.grid(row=3, column=5, sticky=tk.E+tk.W, padx = 10,pady=5,ipadx=10)
    root.withdraw()
    # bg_frame = GradientFrame(root, from_color="#000000", to_color="#E74C3C", height=100)

    main = MainView()
    #main=tk.Frame(root,bg=BACKGROUND)
    #main_view(root)
    root.wm_geometry("400x400")
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()