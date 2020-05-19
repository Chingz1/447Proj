# File description: Scheduler that takes in classes and rooms and creates a schedule
# Takes in 2 arguments: 1st arg - input .xlsx file, 2nd arg - output .xlsx file name
# testing
import pandas as pd
if "pd" not in dir():
    raise ModuleNotFoundError("pandas import error")
import xlrd
if "xlrd" not in dir():
    raise ModuleNotFoundError("xlrd import error")
import sys
if "sys" not in dir():
    raise ModuleNotFoundError("sys import error")
import xlsxwriter
if "xlsxwriter" not in dir():
    raise ModuleNotFoundError("xlsxwriter import error")


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
        self.room = None

    # course object print format
    def __repr__(self):
        if self.room is None:

            return self.subject + " " + str(self.course) + " " + self.professor + " " + str(self.cap)
        else:

            return self.subject + " " + str(self.course) + " " + self.professor + " " + str(self.cap) + ", " + str(self.room)


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

    def __str__(self):
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


class Building(object):
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

    def __repr__(self):
        return self.name + " lat = " + str(self.lat) + "lang = " + str(self.long)

    def __str__(self):
        return self.name + " lat = " + str(self.lat) + "lang = " + str(self.long)


# main: using a given input file creates the best possible schedule taking into account distance and capacity
# Input: a .xlsx file containing a sheet for courses, rooms, and buildings
# Output: a .xlsx file with the schedule, possible alternatives foe unscheduled classes, and statistics related to the schedule
def main():

    # use inline command holding the file name
    file = sys.argv[1]

    # read in input file separated by sheets
    try:
        dataClasses = pd.read_excel(file, sheet_name='Schedule')  # reading file
    except Exception:
        print("Error: There is no table in your classroom file titled 'Schedule'.")
    try:
        dataRooms = pd.read_excel(file, sheet_name='Capacity')  # reading file
    except Exception:
        print("Error: There is no table in your classroom file titled 'Capacity'.")
    try:
        dataBuild = pd.read_excel(file, sheet_name='Coords')  # reading file
    except Exception:
        print("Error: There is no table in your classroom file titled 'Coords'.")

    # convert pandas data frame into raw values
    courses = dataClasses.values
    rooms = dataRooms.values
    buildings = dataBuild.values

    # initialize arrays to hold room and course objects
    courseList = []
    roomList = []
    buildList = []

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

    for i in buildings:
        buildList.append(Building(i[0], i[1], i[2]))

    # sort room list by capacity
    roomList.sort(key=lambda room: room.cap)

    generate_schedule(spring2020, courseList, roomList)
    generate_output(spring2020, courseList)
    print_schedule(spring2020)

# generate_schedule: populates an empty schedule with courses and their rooms as well as create alternatives
# Input: A Schedule object, a list of Course objects, a list of room objects
# Output: None
def generate_schedule(schedule, courses, rooms):
    # loop timeSlots for monday and wednesday
    for i in schedule.mw:
        # loop all courses
        for j in courses:
            # if the course time is for monday/wednesday or monday/wednesday/friday (checking for upper and lower case)
            if j.time == i or "mwf" in j.time:
                # loop through rooms
                for k in rooms:
                    # if the rooms cap is suitable and the room is not taken for the time slot and the course is not scheduled
                    if (j.cap <= k.cap) and not k.taken and not j.shed:
                        # mark rom as taken and course as scheduled
                        j.shed = True
                        j.room = k
                        k.taken = True
                        # add course and room to solution list for monday and wednesday (added as dictionary)
                        schedule.solution[0].append(j)
                        schedule.solution[2].append(j)
                        # if course is also scheduled for friday add to solution list for friday
                        if "mwf" in j.time:
                            schedule.solution[4].append(j)
        # loop over all rooms and reset taken value for next time slot
        for t in rooms:
            # if a room is not taken at a certain time save it for alternatives
            if not t.taken:
                schedule.freeSlots.append({i: t})
            t.taken = False
    # same procedure as above loop but for time slots available tuesday and thursday
    for i in schedule.tt:
        for j in courses:
            if j.time == i:
                for k in rooms:
                    if (j.cap <= k.cap) and not k.taken and not j.shed:
                        j.shed = True
                        j.room = k
                        k.taken = True
                        schedule.solution[1].append(j)
                        schedule.solution[3].append(j)
        for t in rooms:
            if not t.taken:
                schedule.freeSlots.append({i: t})
            t.taken = False

    for i in courses:
        if not i.shed:
            schedule.unScheduled.append(i)

    generate_alternatives(schedule)

    return

# generate_alternatives: finds unscheduled courses the three best alternative times
# Input: A Schedule object
# Output: None
def generate_alternatives(schedule):
    # loop over unscheduled classes
    for course in schedule.unScheduled:
        # loop over available classes
        for slots in schedule.freeSlots:
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

    return


# generate_output: creates an xlsx output file that contains the information of the scheduled and unscheduled classes
# Input: A Schedule object, a list of Course objects
# Output: None
def generate_output(schedule, courses):
    # making a list that formats output info
    output_list = []
    alt_list = []

    # save scheduled courses as strings
    for solution in schedule.solution:
        for every in solution:
            if str(every.ver) == 'nan':
                version = ""
            else:
                version = every.ver
            temp = [every.subject + " " + str(every.course), every.title, version, every.sec, every.professor,
                    every.cap, every.time, str(every.room), "scheduled"]
            if temp not in output_list:
                output_list.append(temp)

    # adding unscheduled courses to the output and alt info list as strings
    for i in courses:
        if not i.shed:
            if str(i.ver) == 'nan':
                version = ""
            else:
                version = i.ver

            temp = [i.subject + " " + str(i.course), i.title, version, i.sec, i.professor, i.cap, "", "",
                    "unscheduled"]
            if temp not in output_list:
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

                if len(schedule.unScheduled[i].alt) != 0:
                    altSheet.write(i, j, str(schedule.unScheduled[i].alt[j - 1]))
                else:
                    altSheet.write(i, j, "No alternatives")

    # close workbook
    out_workbook.close()

    return
# print_schedule: prints a given schedule by days ( for quick debugging purposes only)
# Input: A Schedule object
# Output: printed schedule
def print_schedule(schedule):
    # print solution list for mondays
    print("Monday:")
    for i in schedule.solution[0]:
        print(i)
    # print solution list for tuesdays
    print("Tuesday:")
    for i in schedule.solution[1]:
        print(i)
    # print solution list for wednesdays
    print("Wednesday:")
    for i in schedule.solution[2]:
        print(i)
    # print solution list for thursdays
    print("Thursday:")
    for i in schedule.solution[3]:
        print(i)
    # print solution list for fridays
    print("Friday:")
    for i in schedule.solution[4]:
        print(i)
    # print any unscheduled courses
    print("Unscheduled:")
    # loop over course list and check shed bool
    for i in schedule.unScheduled:
        print(i)

    return


if __name__ == "__main__":
    main()
