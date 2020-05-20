import pandas
import xlsxwriter
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def main(outF):

    #column names of the info needed
    c = ["Time", "Room","Days"]

    #read in the input file needed to generate stats
    filename = "output.xlsx"
    excel_data_df = pandas.read_excel(filename, sheet_name = "Schedule", usecols = c)

    #removes any unschedule classes
    excel_data_df = excel_data_df[excel_data_df['Room'].notna()]
    data = excel_data_df.values.tolist()


    # gets only the names of the rooms
    roomList = []
    for x in data:
        room = x[2]
        if(room not in roomList):
            roomList.append(room)



    #creates a 2d array with the room name and a counter
    timesBooked = []
    for i in roomList:
        info = [i, 0]
        timesBooked.append(info)

    #checks how many times a room has been booked
    for x in timesBooked:
        room = str(x[0])
        count = int(x[1])
        for y in data:
            if room in str(y):
                count+=1

        x[1] = count



    #checks for how many classes are booked on specific days
    days = ["Mon/Wed", "Tues/Thurs", "Mon/Wed/Fri"]
    timesStat = []
    for i in days:
        info = [i, 0]
        timesStat.append(info)


    #iterates through the list and check for each instances of the days
    for y in timesStat:
        name = str(y[0])
        count = int(y[1])
        for z in data:
            if name in str(z):
                y[1] += 1



    # checks for how many hours are booked throughout the day and week
    hours = []
    for i in timesBooked:
        name = i[0]
        day = int(i[1])
        total = day*1.25
        total2 = total*7
        hours.append([name, total, total2])



    # checks for how many classes are booked in each classroom
    # depending on the day of the week
    comp = []
    for x in data:
        if x not in comp:
            comp.sort() #sorts the classrooms by time
            time = x[1]
            name = x[2]
            comp.append([time, name, 0]) # creates an array that stores
                                         # the time, classroom, and counter


    #get rid of duplicates in comp list
    comp = np.unique(comp, axis=0)
    complete = np.array(comp).tolist()


    #creates a new list without the duplicates
    for x in comp:
        t = str(x[0])
        c = str(x[1])
        i = x[2] = int(x[2])
        complete.append([t, c, i])



    counter = 0
    for x in data:
        name = str(x[2]) #gets classroom from output file
        time = str(x[1]) #gets time from output file

        for y in complete:
            name2 = str(y[1])
            time2 = str(y[0])
            y[2] = int(y[2])

            #checks how many times the output appears
            if name == name2 and time == time2:
                y[2] += 1

    #casts name to string
    for x in complete:
        x[2] = str(x[2])


    #create output files
    out_file = "stats_"+ outF
    if os.path.exists(out_file):
        os.remove(out_file)

    #create .xlsx doc
    outname =outF[:len(outF)-5]
    workbook = xlsxwriter.Workbook(out_file)

    #function calls to generate stats
    labs = stat1(timesBooked, workbook, outname)
    stat2(hours, workbook, outname, labs)
    stat3(timesStat, workbook, outname)
    stat4(complete, workbook, outname)



#helper function for pie chart
def func(pct, allvals):
    absolute = int(pct / 100. * np.sum(allvals))
    return "{:.1f}%\n({:d} Classes)".format(pct, absolute)


#ouputs and graphs the number of times a classroom is booked
def stat1(timesBooked, workbook, outname):

    #adds new sheet to excel doc
    sheet = workbook.add_worksheet("Stat1")
    row = 1
    col = 0

    #headers for columns
    sheet.write(0, 0, "Classroom")
    sheet.write(0, 1, "Number of Courses Booked in a Day")

    #temp lists to store x/y axis info for graph
    labels = []
    data = []

    #stats for how many times a classroom is booked in a day
    for x in timesBooked:
        room = str(x[0])
        num = str(x[1])
        sheet.write(row, col, room)
        sheet.write(row, col + 1, num)
        row += 1

        #shorten the classroom names to fit on graph
        labels.append(str(room[:3]+ room[-3:]))
        data.append(int(num))

    #creates the bar graph for the data
    fig1, ax1 = plt.subplots()
    plt.title("Times a Classroom is booked")
    ax1.bar(labels, data)   #plots the bar graph
    plt.xticks(rotation=45) #rotates the labels on x-axis to fit classrooms

    #outputs graph as png
    plt.savefig('stat1_'+outname+'.png', dpi=300, bbox_inches='tight')
    plt.clf()

    #return classrooms for next stat use
    return labels



#stats for how many hours are booked throughout the day and week
def stat2(hours, workbook, outname, labels):

    #add new sheet to excel
    sheet2 = workbook.add_worksheet("Stat2")
    row2 = 1
    col2 = 0

    #create header for columns
    sheet2.write(0, 0, "Classroom")
    sheet2.write(0, 1, "Total Number of Hours per Day")
    sheet2.write(0, 2, "Total Number of Hours per Week")

    #temp lists to store info
    labels2 = []
    data2a = []
    data2b = []

    #writing data to excel sheet
    for x in hours:
        room = str(x[0])
        day = str(x[1])
        week = str(x[2])
        sheet2.write(row2, col2, room)
        sheet2.write(row2, col2 + 1, day)
        sheet2.write(row2, col2 + 2, week)
        row2 += 1

        #shorten classroom names to fit on graph
        labels2.append(str(room[:3] + room[-3:]))
        data2a.append(float(day))
        data2b.append(float(week))

    # formatting the two bars
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, data2a, width, label='day')
    rects2 = ax.bar(x + width / 2, data2b, width, label='week')

    #formatting the graph
    ax.set_ylabel('Number of Course Hours')
    ax.set_title('Total Number of Hours Booked in Each Classroom ')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.legend()
    fig.tight_layout()

    #saving the bar graph as png
    plt.savefig('stat2_' + outname + '.png', dpi=300, bbox_inches='tight')
    plt.clf()



#stats for how many classes are booked on mw/tt/mwf
def stat3(timesStat, workbook, outname):

    #adds sheet to excel
    sheet3 = workbook.add_worksheet("Stat3")
    row3 = 1
    col3 = 0

    #adds column headers
    sheet3.write(0, 0, "Days")
    sheet3.write(0, 1, "Number of Courses Booked")

    #temp lists to store data
    labels3= []
    data3 = []

    #iterates through and populate the columns with data
    for x in timesStat:
        day = str(x[0])
        size = str(x[1])
        sheet3.write(row3, col3, day)
        sheet3.write(row3, col3 + 1, size)
        row3+=1
        labels3.append(day)

        #populates list with the size of the data for pie chart
        data3.append(int(size))

    #creating the pie chart
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax.pie(data3, autopct=lambda pct: func(pct, data3),
                                      textprops=dict(color="w"))

    #formatting the pie chart
    ax.legend(wedges, labels3,
              title="Days",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("Number of Classes Booked Each Day")

    #outputs graph to png
    plt.savefig('stat3_'+outname+'.png', dpi=300, bbox_inches='tight')
    plt.clf()



#stats for how many classes are booked in a class on a day
def stat4(complete, workbook, outname):

    #adds a sheet to excel
    sheet4 = workbook.add_worksheet("Stat4")
    row4 = 1
    col4 = 0

    #add headers to columns
    sheet4.write(0, 0, "Days/Time")
    sheet4.write(0, 1, "Classroom")
    sheet4.write(0, 2, "Number of Courses Booked")

    #iterates through and populate column with data
    for x in complete:
            time = x[0]
            building = x[1]
            count = x[2]
            sheet4.write(row4, col4, time)
            sheet4.write(row4, col4+1, building)
            sheet4.write(row4, col4+2, count)
            row4+=1

    #close excel doc after all stats are written in
    workbook.close()


if __name__ == "__main__":
    main(sys.argv[1])