import pandas
import xlsxwriter
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def main(outF):
    c = ["Time", "Room","Days"]
    filename = outF
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



    #----------------------------------------------------------------
    #This checks for how many times a classroom has been booked
    #
    #
    #----------------------------------------------------------------
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


    #----------------------------------------------------------------
    # This checks for how many classes are booked on specific days
    #
    #----------------------------------------------------------------
    days = ["Mon/Wed", "Tues/Thurs", "Mon/Wed/Fri"]
    timesStat = []
    for i in days:
        info = [i, 0]
        timesStat.append(info)

    for y in timesStat:
        name = str(y[0])
        count = int(y[1])
        for z in data:
            if name in str(z):
                y[1] += 1


    #----------------------------------------------------------------
    # This checks for how many hours are booked throughout the day
    # and week
    #
    #----------------------------------------------------------------
    hours = []
    for i in timesBooked:
        name = i[0]
        day = int(i[1])
        total = day*1.25
        total2 = total*7
        hours.append([name, total, total2])


    #----------------------------------------------------------------
    # This checks for how many classes are booked in each classroom
    # depending on the day of the week (all 2' and 3's)
    #
    #----------------------------------------------------------------
    comp = []
    for x in data:
        if x not in comp:
            comp.sort()

            time = x[1]
            name = x[2]
            comp.append([time, name, 0]) # creates an array that stores
                                             # the time, classroom, and counter

    comp = np.unique(comp, axis=0)
    np.array(comp).tolist()
    complete = np.array(comp).tolist()
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

    for x in complete:
        x[2] = str(x[2])



    #----------------------------------------------------------------
    # Output to excel file
    #----------------------------------------------------------------
    out_file = "stats_"+ outF
    if os.path.exists(out_file):
        os.remove(out_file)
    outname =outF[:len(outF)-5]

    workbook = xlsxwriter.Workbook(out_file)
    labs = stat1(timesBooked, workbook, outname)

    stat2(hours, workbook, outname, labs)
    stat3(timesStat, workbook, outname)
    stat4(complete, workbook, outname)

def func(pct, allvals):
    absolute = int(pct / 100. * np.sum(allvals))
    return "{:.1f}%\n({:d} Classes)".format(pct, absolute)

def stat1(timesBooked, workbook, outname):
    sheet = workbook.add_worksheet("Stat1")
    row = 1
    col = 0
    sheet.write(0, 0, "Classroom")
    sheet.write(0, 1, "Number of Courses Booked in a Day")
    labels = []
    data = []

    #stats for how many times a classroom is booked in a day
    for x in timesBooked:
        room = str(x[0])
        num = str(x[1])
        sheet.write(row, col, room)
        sheet.write(row, col + 1, num)
        row += 1
        labels.append(str(room[:3]+ room[-3:]))
        data.append(int(num))

    fig1, ax1 = plt.subplots()
    plt.title("Times a Classroom is booked")
    ax1.bar(labels, data)
    plt.xticks(rotation=45)
    plt.savefig('stat1_'+outname+'.png', dpi=300, bbox_inches='tight')
    plt.clf()

    return labels

#stats for how many hours are booked throughout the day and week
def stat2(hours, workbook, outname, labels):
    sheet2 = workbook.add_worksheet("Stat2")
    row2 = 1
    col2 = 0
    sheet2.write(0, 0, "Classroom")
    sheet2.write(0, 1, "Total Number of Hours per Day")
    sheet2.write(0, 2, "Total Number of Hours per Week")
    labels2 = []
    data2a = []
    data2b = []
    for x in hours:
        room = str(x[0])
        day = str(x[1])
        week = str(x[2])
        sheet2.write(row2, col2, room)
        sheet2.write(row2, col2 + 1, day)
        sheet2.write(row2, col2 + 2, week)
        row2 += 1
        labels2.append(str(room[:3] + room[-3:]))
        data2a.append(float(day))
        data2b.append(float(week))

    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, data2a, width, label='day')
    rects2 = ax.bar(x + width / 2, data2b, width, label='week')
    ax.set_ylabel('Number of Course Hours')
    ax.set_title('Total Number of Hours Booked in Each Classroom ')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.legend()
    fig.tight_layout()
    plt.savefig('stat2_' + outname + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

#stats for how many classes are booked on mw/tt/mwf
def stat3(timesStat, workbook, outname):
    sheet3 = workbook.add_worksheet("Stat3")
    row3 = 1
    col3 = 0
    sheet3.write(0, 0, "Days")
    sheet3.write(0, 1, "Number of Courses Booked")
    labels3= []
    data3 = []
    for x in timesStat:
        day = str(x[0])
        size = str(x[1])
        sheet3.write(row3, col3, day)
        sheet3.write(row3, col3 + 1, size)
        row3+=1
        labels3.append(day)
        data3.append(int(size))

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))


    wedges, texts, autotexts = ax.pie(data3, autopct=lambda pct: func(pct, data3),
                                      textprops=dict(color="w"))

    ax.legend(wedges, labels3,
              title="Days",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("Number of Classes Booked Each Day")
    plt.savefig('stat3_'+outname+'.png', dpi=300, bbox_inches='tight')
    plt.clf()

def stat4(complete, workbook, outname):
    #stats for how many classes are booked in a class on a day
    sheet4 = workbook.add_worksheet("Stat4")
    row4 = 1
    col4 = 0
    sheet4.write(0, 0, "Time")
    sheet4.write(0, 1, "Classroom")
    sheet4.write(0, 2, "Number of Courses Booked")
    for x in complete:
            time = x[0]
            building = x[1]
            count = x[2]
            sheet4.write(row4, col4, time)
            sheet4.write(row4, col4+1, building)
            sheet4.write(row4, col4+2, count)
            row4+=1

    workbook.close()


if __name__ == "__main__":
    main(sys.argv[1])