# from tkinter import *
import os
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import sys
import pandas as pd

from PIL import Image, ImageTk

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


##class Page1(Page):
 #   def __init__(self, *args, **kwargs):
 #       Page.__init__(self, *args, **kwargs)
  #      label = tk.Label(self, text="Welcome to the Schedule Generator!")
   #     label.pack(side='bottom', anchor=tk.S, fill="both", expand=True)


def on_closing():
    if messagebox.askokcancel("Quit", "Hold up! Closing this window will quit the program. Do you want to quit?"):
        root.destroy()
        sys.exit()


def generate():
    runthis = 'python3 schedule2.py ' + inFile + ' ' + outFile
    os.system(runthis)



def view_schedule():
    master = tk.Tk()
    scrollbar = tk.Scrollbar(master,orient='vertical')
    scrollbarx = tk.Scrollbar(master,orient='horizontal')
    master.title('View Schedule')
    master.configure(bg=BACKGROUND)
    scrollbar.pack(side="right", fill=tk.Y, expand=False)
    scrollbarx.pack(side="bottom",fill=tk.X,expand=False)
    listbox = tk.Listbox(master, xscrollcommand= scrollbarx.set, yscrollcommand=scrollbar.set,bg='white')
    scrollbar.config(command=listbox.yview_scroll)
    scrollbarx.config(command=listbox.xview_scroll)
    #df = pd.read_excel(outFile, sheet_name='Schedule')
    #sched_list = df.values.tolist()
    #print_out_list = {"Scheduled:": [], "Unscheduled:": []}
    #plan: make a label for scheduled and unscheduled, then put scheduled in a list box, then make a button for unscheduled classes?
    s_label = tk.Label(master, text="Scheduled:", bg=BACKGROUND)
    s_label.pack(side='top')
    #header = ["Course","Title","Version","Section","Professor","Capacity","Days","Time","Room","Status"]
    header = ["Course","Title","Professor","Capacity","Days","Time","Room"]
    excel_data_df = pd.read_excel(outFile, sheet_name = "Schedule")
    data = excel_data_df.values.tolist()
    data.insert(0,header)
    for line in data:
        temp_line = ""
        if line[len(line)-1].lower() == "scheduled":
            for val in range(len(line)):
                if val == len(line)-1 or val == 2 or val == 3:
                    temp_line = temp_line                   
                else:
                    temp_line= temp_line + str(line[val])
                    if val == 1:
                        chars = 60
                    elif val == 8:
                        chars = 37
                    else:
                        chars = 24
                    spaces = chars - len(str(line[val]))
                    if spaces < 0:
                        temp_line = temp_line
                    else:
                        temp_line = temp_line + " "*spaces
            listbox.insert(tk.END,temp_line)

    #for i in range(len(sched_list)):
    #    if sched_list[i][len(sched_list[i]) - 1].lower() == "scheduled":
    #        print_out_list["Scheduled:"].append(sched_list[i][:len(sched_list[i]) - 1])
    #    else:
    #        print_out_list["Unscheduled:"].append(sched_list[i][:len(sched_list[i]) - 1])
            
    #for key in print_out_list.keys():
    #    listbox.insert(tk.END, key)
    #    for i in range(len(print_out_list[key])):
    #        listbox.insert(tk.END, str(print_out_list[key][i]))
    #u_button = tk.Button(master, text="Unscheduled", highlightthickness=0, padx=5, bg=GOLD)
    listbox.pack(side="top", fill=tk.BOTH, expand=True)
    #u_button.pack(side="top")

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
        b3 = tk.Button(self, text="View Statistics", command=self.view_stats, highlightthickness=0,bg=GOLD)  # , command=p3.lift)
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
        
    def view_stats(self):
        self.stats = tk.Toplevel(self,bg=BACKGROUND)
        self.stats.title('Statistics')
        tk.Grid.rowconfigure(self.stats, 0, weight=1)
        tk.Grid.columnconfigure(self.stats, 0, weight=1)
        
        #Create & Configure frame 
        frame=tk.Frame(self.stats,bg=BACKGROUND)
        frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        for row_index in range(6):
            tk.Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(5):
                tk.Grid.columnconfigure(frame, col_index, weight=1)
        self.stats_file = "stats_"+outFile
        print(self.stats_file)
        self.stat1_pic = "stat1_"+outFile[:len(outFile)-4]+"png"
        self.stat2_pic = "stat2_"+outFile[:len(outFile)-4]+"png"
        self.stat3_pic = "stat3_"+outFile[:len(outFile)-4]+"png"
        print(self.stat1_pic)
        
        title_label = tk.Label(frame, text="Statistics for the Schedule", font=("Helvetica", 32),fg='white',bg='black')
        title_label.grid(row=0, column=0,columnspan=6, sticky=tk.N+tk.S+tk.E+tk.W)
        
        #print out stat1 photo
        photo1 = ImageTk.PhotoImage(Image.open(self.stat1_pic).resize((300, 300), Image.ANTIALIAS ))
        stat1 = tk.Label(frame, image=photo1,bg=BACKGROUND)
        stat1.image = photo1 # keep a reference!
        stat1.grid(row=2, column=1, sticky=tk.E+tk.W+tk.S+tk.N)
        
        #print out stat2 photo
        photo2 = ImageTk.PhotoImage(Image.open(self.stat2_pic).resize((300, 300), Image.ANTIALIAS ))
        stat2 = tk.Label(frame, image=photo2,bg=BACKGROUND)
        stat2.image = photo2 # keep a reference!
        stat2.grid(row=2, column=3, sticky=tk.E+tk.W+tk.S+tk.N)
        
        #print out stat3 photo
        photo3 = ImageTk.PhotoImage(Image.open(self.stat3_pic).resize((350, 300), Image.ANTIALIAS ))
        stat3 = tk.Label(frame, image=photo3,bg=BACKGROUND)
        stat3.image = photo3 # keep a reference!
        stat3.grid(row=2, column=2, sticky=tk.E+tk.W+tk.S+tk.N)
        
        b_stat1 = tk.Button(frame, text="Room usage by Time", command=self.stat1_out, bg=GOLD)
        b_stat1.grid(row=3, column=1, sticky=tk.E+tk.W+tk.S+tk.N)
        b_stat2 = tk.Button(frame, text="Hours in Rooms", command=self.stat2_out, bg=GOLD)
        b_stat2.grid(row=3, column=3, sticky=tk.E+tk.W+tk.S+tk.N)
        b_stat3 = tk.Button(frame, text="Classes per Day", command=self.stat3_out, bg=GOLD)
        b_stat3.grid(row=3, column=2, sticky=tk.E+tk.W+tk.S+tk.N)
        b_stat4 = tk.Button(frame, text="Classes booked per Room and Time", command=self.stat4_out, bg=GOLD)
        b_stat4.grid(row=4, column=1,columnspan=3, sticky=tk.E+tk.W+tk.S+tk.N)
        
    def stat1_out(self):
        self.stats1 = tk.Toplevel(self.stats,bg=BACKGROUND)
        self.stats1.title('Room usage by Time')
        tk.Grid.rowconfigure(self.stats1, 0, weight=1)
        tk.Grid.columnconfigure(self.stats1, 0, weight=1)
        
        #Create & Configure frame 
        frame=tk.Frame(self.stats1,bg=BACKGROUND)
        frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        header = ["Classroom","Number of Courses Booked in a Day"]
        excel_data_df = pd.read_excel(self.stats_file, sheet_name = "Stat1")
        data = excel_data_df.values.tolist()
        print(data)
        for row_index in range(len(data)):
            tk.Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(len(header)):
                tk.Grid.columnconfigure(frame, col_index, weight=1)
                if row_index == 0:
                    tk.Label(frame, text=header[col_index], bg=BACKGROUND).grid(row=row_index, column=col_index, sticky=tk.N+tk.S,padx=5,pady=5)
                else:
                    tk.Label(frame, text=data[col_index], bg=BACKGROUND).grid(row=row_index, column=col_index, sticky=tk.N+tk.S,padx=5,pady=5)
    
    def stat2_out(self):
        self.stats2 = tk.Toplevel(self.stats,bg=BACKGROUND)
        self.stats2.title('Hours in Rooms')
        tk.Grid.rowconfigure(self.stats2, 0, weight=1)
        tk.Grid.columnconfigure(self.stats2, 0, weight=1)
        
        #Create & Configure frame 
        frame=tk.Frame(self.stats2,bg=BACKGROUND)
        frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        header = ["Classroom","Total Number of Hours per Day","Total Number of Hours per Week"]     
        excel_data_df = pd.read_excel(self.stats_file, sheet_name = "Stat2")
        data = excel_data_df.values.tolist()
        print(data)
        for row_index in range(len(data)):
            tk.Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(len(header)):
                tk.Grid.columnconfigure(frame, col_index, weight=1)
                if row_index == 0:
                    tk.Label(frame, text=header[col_index], bg=BACKGROUND).grid(row=row_index, column=col_index, sticky=tk.N+tk.S,padx=5,pady=5)
                else:
                    tk.Label(frame, text=data[col_index], bg=BACKGROUND).grid(row=row_index, column=col_index, sticky=tk.N+tk.S,padx=5,pady=5)

    def stat3_out(self):
        self.stats3 = tk.Toplevel(self.stats,bg=BACKGROUND)
        self.stats3.title('Classes per Day')
        tk.Grid.rowconfigure(self.stats3, 0, weight=1)
        tk.Grid.columnconfigure(self.stats3, 0, weight=1)
        
        #Create & Configure frame 
        frame=tk.Frame(self.stats3,bg=BACKGROUND)
        frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        header = ["Days","Number of Courses Booked"]     
        excel_data_df = pd.read_excel(self.stats_file, sheet_name = "Stat3")
        data = excel_data_df.values.tolist()
        print(data)
        for row_index in range(len(data)):
            tk.Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(len(header)):
                tk.Grid.columnconfigure(frame, col_index, weight=1)
                if row_index == 0:
                    tk.Label(frame, text=header[col_index], bg=BACKGROUND).grid(row=row_index, column=col_index, sticky=tk.N+tk.S,padx=5,pady=5)
                else:
                    tk.Label(frame, text=data[col_index], bg=BACKGROUND).grid(row=row_index, column=col_index, sticky=tk.N+tk.S,padx=5,pady=5)
        
    def stat4_out(self):
        self.stats4 = tk.Toplevel(self.stats,bg=BACKGROUND)
        self.stats4.title('Classes booked per Room and Time')
        scrollbar = tk.Scrollbar(self.stats4)
        scrollbar.pack(side="right", fill=tk.Y, expand=False)
        listbox = tk.Listbox(self.stats4, yscrollcommand=scrollbar.set,bg=BACKGROUND)

        header = ["Days/Time","Classroom","Number of Courses Booked"]
        excel_data_df = pd.read_excel(self.stats_file, sheet_name = "Stat4")
        data = excel_data_df.values.tolist()
        data.insert(0,header)
        for line in data:
            temp_line = ""
            for val in line:
                temp_line= temp_line + str(val)
                spaces = 19 - len(str(val))
                if spaces < 0:
                    temp_line = temp_line
                else:
                    temp_line = temp_line + " "*spaces
            listbox.insert(tk.END,temp_line)

        listbox.pack(side="left", fill=tk.BOTH, expand=True)
    
        scrollbar.config(command=listbox.yview_scroll)
        
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