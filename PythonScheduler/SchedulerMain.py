import pandas as pd
import xlrd
import sys
import tabulate

# Course object
class Course(object):
    # bool representing if course has been scheduled or not set to False by default
    shed = False

    # Course constructor
    def __init__(self, subject, course, title, ver, sec, professor, time, cap):
        self.subject = subject
        self.course = course
        self.title = title
        self.ver = ver
        self.sec = sec
        self.professor = professor
        self.time = time
        self.cap = cap

    # course object print format
    def __repr__(self):
        return self.subject + " " + str(self.course) + " " + self.professor + " " + str(self.cap) + " " + self.time

# room object
class Room(object):
    # bool representing if room is in use or not false by default and is reset for every time slot
    taken = False

    # room constructor
    def __init__(self, name, cap):
        self.name = name
        self.cap = cap

    # room object print format
    def __repr__(self):
        return self.name

# schedule object
class Schedule(object):

    # list to hold time slots available per day
    mw = []  # monday & wednesday
    tt = []  # tuesday & thursday
    mwf = []  # monday, wednesday & friday

    #  1 X 5 2D array that hold final solution each internal array representing a day of the week
    solution = [[], [], [], [], []]


# use inline command holding the file name
file = sys.argv[1]

# read in input file separated by sheets
dataClasses = pd.read_excel(file, sheet_name='Schedule')  # reading file
dataRooms = pd.read_excel(file, sheet_name='Capacity')  # reading file

# convert pandas data frame into raw values
courses = dataClasses.values
rooms = dataRooms.values

# initialize arrays to hold room and course objects
courseList = []
roomList = []

# create schedule object
spring2020 = Schedule()

# import time slots into schedule based on days
for i in dataClasses.Time:

    # if statement to separate slots based on days and to avoid repeats
    if (("mw" in i) or ("MW" in i)) and not (i in spring2020.mw):
        spring2020.mw.append(i)
    if (("tt" in i) or ("TT" in i)) and not (i in spring2020.tt):
        spring2020.tt.append(i)
    if (("MWF" in i) or("mwf" in i)) and not (i in spring2020.mwf):
        spring2020.mwf.append(i)

# create courses and add to Course list
for i in courses:
    courseList.append(Course(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

# create rooms and add to room list
for i in rooms:
    roomList.append(Room(i[0], i[1]))

# sort room list by capacity
roomList.sort(key = lambda room: room.cap)

# loop timeSlots for monday and wednesday
for i in spring2020.mw:
    # loop all courses
    for j in courseList:
        # if the course time is for monday/wednesday or monday/wednesday/friday (checking for upper and lower case)
        if (j.time == i) or (j.time.upper() == i ) or ("MWF" in j.time) or ("mwf" in j.time):
            # loop through rooms
            for k in roomList:
                # if the rooms cap is suitable and the room is not taken for the time slot and the course is not scheduled
                if (j.cap <= k.cap) and not (k.taken) and not (j.shed):
                    # mark rom as taken and course as scheduled
                    j.shed = True
                    k.taken = True
                    # add course and room to solution list for monday and wednesday (added as dictionary)
                    spring2020.solution[0].append({j: k})
                    spring2020.solution[2].append({j: k})
                    # if course is also scheduled for friday add to solution list for friday
                    if ("MWF" in j.time) or ("mwf" in j.time):
                        spring2020.solution[4].append({j: k})
    # loop over all rooms and reset taken value for next timeslot
    for t in roomList:
        t.taken = False
# same procedure as above loop but for timeslots available tuesday and thursday
for i in spring2020.tt:
    for j in courseList:
        if (j.time == i) or (j.time.upper() == i):
            for k in roomList:
                if (j.cap <= k.cap) and not (k.taken) and not (j.shed):
                    j.shed = True
                    k.taken = True
                    spring2020.solution[1].append({j: k})
                    spring2020.solution[3].append({j: k})
    for t in roomList:
        t.taken = False




# for i in range(len(spring2020.solution)):
#     print(days[i])
#     for j in spring2020.solution[i]:
#         print(j)

booked = 0;
days = len(spring2020.solution)
roomCheck = []
all = []
capacity = 0
for i in range(days):
    for j in spring2020.solution[i]:
       all.append(j)

# for i in range(len(all)):
#     header = all[i].values()
#     rows = [x.keys() for x in all]
#     temp = str(header)
#     capacity = len(temp)
#     if (temp not in roomCheck):
#         roomCheck.append(temp)
#         booked += 1
#
#
#     print(tabulate.tabulate(rows, header, tablefmt="pretty"))
#     print(capacity, "Classes Booked in ", temp, "\n\n\n")

for i in range(days):
    for j in spring2020.solution[i]:
        header = j.values()
        rows = [x.keys() for x in spring2020.solution[i]]
        temp = str(header)

        if (temp not in roomCheck):
            roomCheck.append(temp)
            booked += 1

        capacity = len(spring2020.solution[i])
        print(tabulate.tabulate(rows, header, tablefmt="pretty"))
        print(capacity, "Classes Booked in ", temp, "\n\n\n")


print("***There are", booked, "classrooms in use***", "\n")


# print any unscheduled courses
print("Unscheduled:")
# loop over course list and check shed bool
for i in courseList:
    if (not (i.shed)):
        print(i)