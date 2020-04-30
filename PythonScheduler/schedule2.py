# File description: Scheduler that takes in classes and rooms and creates a schedule
# Takes in 2 arguments: 1st arg - input xlsx file, 2nd arg - output xlsx file name
# testing
import pandas as pd
if "pd" not in dir():
    raise ImportError("Pandas not imported")
import xlrd
if "xlrd" not in dir():
    raise ImportError("xlrd not imported")
import sys
if "sys" not in dir():
    raise ImportError("sys not imported")
import xlsxwriter
if "xlsxwriter" not in dir():
    raise ImportError("xlsxwriter not imported")


# Course object
class Course(object):

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
        # list of 3 possible alternatives
        self.alt = []
        # bool representing if course has been scheduled or not set to False by default
        self.shed = False

    # course object print format
    def __repr__(self):
        return self.subject + " " + str(self.course) + " " + self.professor + " " + str(self.cap)


# room object
class Room(object):
    # bool representing if room is in use or not false by default and is reset for every time slot
    taken = False
    # usage hours for statistics
    hours = 0

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

    freeSlots = []  # available alternatives

    #  1 X 5 2D array that hold final solution each internal array representing a day of the week
    solution = [[], [], [], [], []]
    unScheduled = []


# generate_output: creates an xlsx output file that contains the information of the scheduled and unscheduled classes
# Input: A Schedule object, a list of Course objects
# Output: None
def generate_output(schedule, courses):
    # making a list that formats output info
    output_list = []
    alt_list = []

    # save scheduled courses as strings
    for solution in schedule.solution:
        for i in solution:
            for every in i.keys():
                if str(every.ver) == 'nan':
                    version = ""
                else:
                    version = every.ver
                temp = [every.subject + " " + str(every.course), every.title, version, every.sec, every.professor,
                        every.cap, every.time, str(i[every]), "scheduled"]
                output_list.append(temp)

    # adding unscheduled courses to the output and alt info list as strings
    for i in courses:
        if (not (i.shed)):
            if str(i.ver) == 'nan':
                version = ""
            else:
                version = i.ver
        
            temp = [i.subject + " " + str(i.course), i.title, version, i.sec, i.professor, i.cap, i.time, "",
                    "unscheduled"]
            output_list.append(temp)

            temp = [i.subject + " " + str(i.course) + i.title + str(i.sec) + i.professor]
            alt_list.append(temp)


    # writing to output excel workbook file that the user specifies as the second argument
    out_workbook = xlsxwriter.Workbook(sys.argv[2])
    # create sheet and header schedule
    scheduleSheet = out_workbook.add_worksheet('Schedule')
    Sheader = ["Course", "Title", "Version", "Section", "Professor", "Capacity", "Time", "Room", "Status"]
    # add schedule
    for i in range(len(output_list)):
        for j in range(len(output_list[i])):
            if i == 0:
                scheduleSheet.write(i, j, Sheader[j])

            else:
                scheduleSheet.write(i, j, output_list[i][j])

    # create alternatives sheet and header
    altSheet = out_workbook.add_worksheet('Alternatives')
    Aheader = ["course", "alt1", "alt2", "alt3"]

    # add alternatives
    for i in range(len(alt_list)):
        for j in range(len(Aheader)):
            if i == 0:
                altSheet.write(i, j, Aheader[j])

            elif j == 0:

                altSheet.write(i, j, alt_list[i][j])
            else:

                if len(spring2020.unScheduled[i].alt) != 0:
                    altSheet.write(i,j, str(spring2020.unScheduled[i].alt[j-1]))
                else:
                    altSheet.write(i, j,"No alternatives")

    # close workbook
    out_workbook.close()


# use inline command holding the file name
file = sys.argv[1]

# read in input file separated by sheets
dataClasses = pd.read_excel(file, sheet_name='Schedule')# reading file
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
        spring2020.mw.append(i.lower())
    if (("tt" in i) or ("TT" in i)) and not (i in spring2020.tt):
        spring2020.tt.append(i.lower())

    if (("MWF" in i) or("mwf" in i)) and not (i in spring2020.mwf):
        spring2020.mwf.append(i.lower())

# create courses and add to Course list
for i in courses:
    courseList.append(Course(i[0], i[1], i[2], i[3], i[4], i[5], i[6].lower(), i[7]))

# create rooms and add to room list
for i in rooms:
    roomList.append(Room(i[0], i[1]))

# sort room list by capacity
roomList.sort(key=lambda room: room.cap)

# loop timeSlots for monday and wednesday
for i in spring2020.mw:
    # loop all courses
    for j in courseList:
        # if the course time is for monday/wednesday or monday/wednesday/friday (checking for upper and lower case)
        if j.time == i or "mwf" in j.time:
            # loop through rooms
            for k in roomList:
                # if the rooms cap is suitable and the room is not taken for the time slot and the course is not scheduled
                if (j.cap <= k.cap) and not (k.taken) and not (j.shed):
                    # mark rom as taken and course as scheduled
                    j.shed = True
                    k.taken = True
                    # add usage to room
                    k.hours += 2.5
                    # add course and room to solution list for monday and wednesday (added as dictionary)
                    spring2020.solution[0].append({j: k})
                    spring2020.solution[2].append({j: k})
                    # if course is also scheduled for friday add to solution list for friday
                    if "mwf" in j.time:
                        k.hours += 1.25
                        spring2020.solution[4].append({j: k})
    # loop over all rooms and reset taken value for next time slot
    for t in roomList:
        # if a room is not taken at a certain time save it for alternatives
        if not t.taken:
            spring2020.freeSlots.append({i: t})
        t.taken = False
# same procedure as above loop but for time slots available tuesday and thursday
for i in spring2020.tt:
    for j in courseList:
        if j.time == i:
            for k in roomList:
                if (j.cap <= k.cap) and not (k.taken) and not (j.shed):
                    j.shed = True
                    k.taken = True
                    k.hours += 2.5
                    spring2020.solution[1].append({j: k})
                    spring2020.solution[3].append({j: k})
    for t in roomList:
        if not t.taken:
            spring2020.freeSlots.append({i: t})
        t.taken = False

for i in courseList:
    if not i.shed:
        spring2020.unScheduled.append(i)

# print solution list for mondays
print("Monday:")
for i in spring2020.solution[0]:
    print(i)
# print solution list for tuesdays
print("Tuesday:")
for i in spring2020.solution[1]:
    print(i)
# print solution list for wednesdays
print("Wednesday:")
for i in spring2020.solution[2]:
    print(i)
# print solution list for thursdays
print("Thursday:")
for i in spring2020.solution[3]:
    print(i)
# print solution list for fridays
print("Friday:")
for i in spring2020.solution[4]:
    print(i)
# print any unscheduled courses
print("Unscheduled:")
# loop over course list and check shed bool
for i in spring2020.unScheduled:
    print(i)


# loop over unscheduled classes
for course in spring2020.unScheduled:
    # loop over available classes
    for slots in spring2020.freeSlots:
        # for time slots in free spaces
        for keys in slots:
            # try and fit into the same days as professor originally asked for
            if course.time == keys and course.cap <= slots[keys].cap:
                course.alt.append(slots)
            # if not fit into first slot found
            elif slots[keys].cap >= course.cap:
                course.alt.append(slots)
        # limit to 3 alternatives max
        if len(course.alt) > 2:
            break


generate_output(spring2020, courseList)




