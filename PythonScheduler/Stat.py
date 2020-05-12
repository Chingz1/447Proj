import pandas
import xlsxwriter
import os
import sys
c = ["Time", "Room"]
filename = sys.argv[1]
excel_data_df = pandas.read_excel(filename, sheet_name = "Schedule", usecols = c)

#removes any unschedule classes
excel_data_df = excel_data_df[excel_data_df['Room'].notna()]
data = excel_data_df.values.tolist()

# gets only the names of the rooms
roomList = []
for x in data:
    room = x[1]
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

print("TimesBooked", timesBooked)




#----------------------------------------------------------------
# This checks for how many classes are booked on specific days
#
#----------------------------------------------------------------
days = ["mw", "tt", "mwf"]
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

print("size", timesStat)



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
    hours.append([name, str(total) +" hrs in a day", str(total2) + " hrs per week"])
print("Hours", hours)



#----------------------------------------------------------------
# This checks for how many classes are booked in each classroom
# depending on the day of the week (all 2' and 3's)
#
#----------------------------------------------------------------
complete = []
for x in data:
    if x not in complete:
        time = x[0]
        name = x[1]
        complete.append([time, name, 0]) # creates an array that stores
                                         # the time, classroom, and counter


counter = 0
for x in data:
    name = str(x[1]) #gets classroom from output file
    time = str(x[0]) #gets time from output file

    for y in complete:
        name2 = str(y[1])
        time2 = str(y[0])
        y[2] = int(y[2])

        #checks how many times the output appears
        if name == name2 and time == time2:
            #print(name, name2, time, time2)
            y[2] += 1

for x in complete:
    x[2] = str(x[2])

#removes duplicates
res = list(set(map(lambda i: tuple(sorted(i)), complete)))

# for y in complete:
#     print(y)
print("complete", complete)



#----------------------------------------------------------------
# Output to excel file
# I could only run the Stat program once, if I ran it again it will
# throw an error. The error can be fixed by deleting the tests.xlsx
# file and running the program again - ching
#^i think i fixed it - anna
#----------------------------------------------------------------
out_file = "stats_"+sys.argv[1]
if os.path.exists(out_file):
    os.remove(out_file)
workbook = xlsxwriter.Workbook(out_file)
sheet = workbook.add_worksheet("Stat1")
row = 0
col = 0

#stats for how many times a classroom is booked in a day
for x in timesBooked:
    room = str(x[0])
    num = str(x[1])
    sheet.write(row, col, room)
    sheet.write(row, col + 1, num)
    row += 1


#stats for how many hours are booked throughout the day and week
sheet2 = workbook.add_worksheet("Stat2")
row2 = 0
col2 = 0
for x in hours:
    room = str(x[0])
    day = str(x[1])
    week = str(x[2])
    sheet2.write(row2, col2, room)
    sheet2.write(row2, col2 + 1, day)
    sheet2.write(row2, col2 + 2, week)
    row2+=1

#stats for how many classes are booked on mw/tt/mwf
sheet3 = workbook.add_worksheet("Stat3")
row3 = 0
col3 = 0
for x in timesStat:
    day = str(x[0])
    size = str(x[1])
    sheet3.write(row3, col3, day)
    sheet3.write(row3, col3 + 1, size)
    row3+=1

#stats for how many classes are booked in a class on a day
sheet4 = workbook.add_worksheet("Stat4")
row4 = 0
col4 = 0
for x in complete:
        time = x[0]
        building = x[1]
        count = x[2]
        sheet4.write(row4, col4, time)
        sheet4.write(row4, col4+1, building)
        sheet4.write(row4, col4+2, count)
        row4+=1

workbook.close()



