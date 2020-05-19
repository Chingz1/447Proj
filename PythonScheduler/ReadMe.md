# Python Scheduler
> Our product takes in class and room data for the UMBC Campus and assigns classes to rooms based on the class’s professor, subject, and capacity requirements. Our software is programmed in python and includes its own user friendly GUI that allows the user to report errors, generate the schedule, view the generated schedule, provide alternatives, and view statistical information such as room usage. Finally our program outputs the generated schedule into a xlsx file for future use.

## Setup 
* Download a Python3 environment, we recommend Anaconda, but you’re welcome to download any Python3 environment: https://docs.anaconda.com/anaconda/install/
* Required Libraries: Pandas, Matplotlib, Xlsxwriter, Tkinter, Sys,OS, Time, Numpy, Pillow, Geopy, and DayTime
* Once Anaconda complete its installation, install the libraries by opening up the Anaconda prompt, which you can access by searching up Anaconda on the Windows search bar.
* After successfully installing all of the required libraries, download our scheduling software from Github and save the files to a location that you can easily access
* Once the scheduling software is downloaded, open up Jupyter Notebook which comes prepackaged with Anaconda. Jupyter Notebook can be accessed in the same manner as Anaconda, simply search it up on the Windows search bar
* The folder should contain all of the files from our Github repository, if not return to the Github page and redownload the folder.
* Run the project by running the following in a Jupyter Notebook
`!python3 scheduler_gui.py`

## Features
* Generate a schedule
* View schedule
* Manage alternative time slots
* View stastics 
