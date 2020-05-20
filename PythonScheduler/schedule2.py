# File description: Scheduler that takes in classes and rooms and creates a schedule
# Takes in 2 arguments: 1st arg - input .xlsx file, 2nd arg - output .xlsx file name
# testing
import pandas as pd

if "pd" not in dir():
    raise ModuleNotFoundError("pandas import error")

import sys

if "sys" not in dir():
    raise ModuleNotFoundError("sys import error")

import xlsxwriter

if "xlsxwriter" not in dir():
    raise ModuleNotFoundError("xlsxwriter import error")
import datetime

if "datetime" not in dir():
    raise ModuleNotFoundError("datetime import error")
from geopy.distance import geodesic
import Stat
import copy


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
        self.days = None
        self.Mtime = None

    # course object print format
    def __repr__(self):
        if self.room is None:

            return self.subject + " " + str(self.course) + " " + self.professor + " " + str(self.sec)
        else:

            return self.subject + " " + str(self.course) + " " + self.professor + " " + str(self.sec) + ", " + str(
                self.room) + " " + str(self.Mtime)


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
    def __init__(self):
        self.mw = []  # monday & wednesday
        self.tt = []  # tuesday & thursday
        self.mwf = []  # monday, wednesday & friday
        self.freeSlots = []  # available alternatives
        #  1 X 5 2D array that hold final solution each internal array representing a day of the week
        self.solution = [[], [], [], [], []]
        self.unScheduled = []


class Building(object):

    def __init__(self, name, lat, long, subject):
        # Name of building
        self.name = name
        # buildings latitude and longitude
        self.lat = lat
        self.long = long
        # subject associated with building
        self.subject = subject

    def __repr__(self):
        return self.name + " lat = " + str(self.lat) + "lang = " + str(self.long) + self.subject

    def __str__(self):
        return self.name + " lat = " + str(self.lat) + "lang = " + str(self.long) + self.subject


# main: using a given input file creates the best possible schedule taking into account distance and capacity
# Input: a .xlsx file containing a sheet for courses, rooms, and buildings
# Output: a .xlsx file with the schedule, possible alternatives foe unscheduled classes, and statistics related to the schedule
def main(inF, outF):
    # use inline command holding the file name
    file = inF

    # read in input file separated by sheets
    try:
        dataClasses = pd.read_excel(file, sheet_name='Schedule')  # reading file
    except Exception:
        raise Exception("Error: There is no table in your classroom file titled 'Schedule'.")
    try:
        dataRooms = pd.read_excel(file, sheet_name='Capacity')  # reading file
    except Exception:
        raise Exception("Error: There is no table in your classroom file titled 'Capacity'.")
    try:
        dataBuild = pd.read_excel(file, sheet_name='Coords')  # reading file
    except Exception:
        raise Exception("Error: There is no table in your classroom file titled 'Coords'.")

    # convert pandas data frame into raw values
    courses = dataClasses.values
    rooms = dataRooms.values
    buildings = dataBuild.values

    # initialize arrays to hold room and course objects
    courseList = []
    roomList = []
    buildList = []
    subjectTobuilding = {}

    # create schedule object
    spring2020 = Schedule()

    # import time slots into schedule based on days
    for i in dataClasses.Time:
        # if statement to separate slots based on days and to avoid repeats
        if (("mw" in i) or ("MW" in i)) and not (i in spring2020.mw):
            spring2020.mw.append(i.lower())
        if (("tt" in i) or ("TT" in i)) and not (i in spring2020.tt):
            spring2020.tt.append(i.lower())

        if (("MWF" in i) or ("mwf" in i)) and not (i in spring2020.mwf):
            spring2020.mwf.append(i.lower())

    # create courses and add to Course list
    for i in courses:
        # (self, subject, course, title, ver, sec, professor, time, cap):
        courseList.append(Course(i[0], str(i[1]), i[2], i[3], i[4], i[5], i[6].lower(), i[7]))

    # convert given time value into to an easier to read and understand format
    for i in courseList:
        if "mw" in i.time:
            if "mwf" in i.time:
                i.days = "Mon/Wed/Fri"
                temp = i.time.split("mwf")
                i.Mtime = convert_Time(temp)
            else:
                i.days = "Mon/Wed"
                temp = i.time.split("mw")
                i.Mtime = convert_Time(temp)
        if "tt" in i.time:
            i.days = "Tues/Thurs"
            temp = i.time.split("tt")
            i.Mtime = convert_Time(temp)

    # create rooms and add to room list
    for i in rooms:
        roomList.append(Room(i[0], i[1]))

    # create building objects and add them to list
    for i in range(len(buildings)):
        buildList.append(Building(buildings[i][0], buildings[i][1], buildings[i][2], buildings[i][3]))
        subjectTobuilding[buildList[i].subject] = buildList[i].name

    # warning file for error output during schedule generation
    warningTextFile = "warning.txt"
    fo = open(warningTextFile, "w")
    fo.write("Warnings:\n")
    fo.close()

    # make 5 copies of schedule, courseList, and roomList
    S1 = copy.deepcopy(spring2020)
    S1c = copy.deepcopy(courseList)
    S1r = copy.deepcopy(roomList)
    S2 = copy.deepcopy(spring2020)
    S2c = copy.deepcopy(courseList)
    S2r = copy.deepcopy(roomList)
    S3 = copy.deepcopy(spring2020)
    S3c = copy.deepcopy(courseList)
    S3r = copy.deepcopy(roomList)
    S4 = copy.deepcopy(spring2020)
    S4c = copy.deepcopy(courseList)
    S4r = copy.deepcopy(roomList)
    S5 = copy.deepcopy(spring2020)
    S5c = copy.deepcopy(courseList)
    S5r = copy.deepcopy(roomList)

    # First generated schedule rooms and courses in given order
    generate_schedule(S1, S1c, S1r, buildList, subjectTobuilding)
    # set main schedule to S1
    spring2020 = copy.deepcopy(S1)
    courseList = copy.deepcopy(S1c)

    # organize courseList by capacity
    S2c.sort(key=lambda course: course.cap)

    # second generated schedule room in given order courseList organized by cap G -> L
    generate_schedule(S2, S2c, S2r, buildList, subjectTobuilding)
    # if schedule has less unscheduled classes than spring2020 make this spring 2020
    if len(S2.unScheduled) < len(spring2020.unScheduled):
        spring2020 = copy.deepcopy(S2)
        courseList = copy.deepcopy(S2c)

    S3c.sort(key=lambda course: course.cap, reverse=True)
    # third generated schedule room in given order courseList organized by cap L -> G
    generate_schedule(S3, S3c, S3r, buildList, subjectTobuilding)
    if len(S3.unScheduled) < len(spring2020.unScheduled):
        spring2020 = copy.deepcopy(S3)
        courseList = copy.deepcopy(S3c)

    # sort room list by capacity
    S4r.sort(key=lambda room: room.cap)

    S4c.sort(key=lambda course: course.cap)
    # fourth generated schedule room organized by cap G -> l courseList organized by cap G -> l
    generate_schedule(S4, S4c, S4r, buildList, subjectTobuilding)
    if len(S4.unScheduled) < len(spring2020.unScheduled):
        spring2020 = copy.deepcopy(S4)
        courseList = copy.deepcopy(S4c)

    S5c.sort(key=lambda course: course.cap, reverse=True)
    S5r.sort(key=lambda room: room.cap)

    # fourth generated schedule room organized by cap G -> l courseList organized by cap L -> G
    generate_schedule(S5, S5c, S5r, buildList, subjectTobuilding)
    if len(S5.unScheduled) < len(spring2020.unScheduled):
        spring2020 = copy.deepcopy(S5)
        courseList = copy.deepcopy(S5c)

    # sort spring 2020 by time in days
    spring2020.solution[0].sort(key=lambda course: course.Mtime.hour)
    spring2020.solution[1].sort(key=lambda course: course.Mtime.hour)
    spring2020.solution[2].sort(key=lambda course: course.Mtime.hour)
    spring2020.solution[3].sort(key=lambda course: course.Mtime.hour)
    spring2020.solution[4].sort(key=lambda course: course.Mtime.hour)

    # write schedule to output file
    generate_output(spring2020, courseList, outF)
    # print_schedule(spring2020)
    Stat.main(outF)


# generate_schedule: populates an empty schedule with courses and their rooms as well as create alternatives
# Input: A Schedule object, a list of Course objects, a list of room objects, a  list  of buildings and a dict correlating subjects to building
# Output: None
def generate_schedule(schedule, courses, rooms, buildings, subjectToBuilding):
    # loop timeSlots for monday and wednesday
    # list of professors to avoid professors teaching multiple classes at the same time
    professors = []

    # loop over  monday, wednesday and friday time slots
    for i in schedule.mw:
        # clear professors for current time slot
        professors.clear()
        # loop over courses
        for j in courses:
            # if current time slot matches courses
            if i == j.time or "mwf" in j.time:
                # calculate weights for all rooms
                weights = calculateRoomWeights(j, rooms, {}, subjectToBuilding, 500, "warning.txt", buildings)
                # index for current best room
                bestRoom = weights.index(max(weights))
                # current highest weight
                w = max(weights)
                # temp weight list that we can edit without worry
                temp = list(weights)
                # while course is not scheduled
                while not j.shed:
                    # if professor is already teaching in this slot break
                    if j.professor in professors:
                        break

                    if w <= 0:
                        break
                    # if best room is taken remove it form list and find next best room if one is available otherwise break
                    if rooms[bestRoom].taken:
                        del temp[temp.index(max(temp))]
                        if len(temp) == 0:
                            break
                        w = max(temp)
                        if w <= 0:
                            break
                        bestRoom = weights.index(max(temp))

                    # if current best room is free schedule course and add to appropriate list
                    else:
                        j.shed = True
                        j.room = rooms[bestRoom]
                        rooms[bestRoom].taken = True
                        if j.professor != "Staff":
                            professors.append(j.professor)

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
            else:
                t.taken = False

    # exact same as above loop instead looping over tuesday thursday time slots
    for i in schedule.tt:
        professors.clear()
        for j in courses:
            if i == j.time:

                weights = calculateRoomWeights(j, rooms, {}, subjectToBuilding, 500, "warning.txt", buildings)
                bestRoom = weights.index(max(weights))
                w = max(weights)
                temp = list(weights)
                while not j.shed:
                    if j.professor in professors:
                        break

                    if w == 0:
                        break
                    if rooms[bestRoom].taken:
                        del temp[temp.index(max(temp))]
                        if len(temp) == 0:
                            break
                        w = max(temp)
                        if w <= 0:
                            break
                        bestRoom = weights.index(max(temp))
                    else:
                        j.shed = True
                        j.room = rooms[bestRoom]
                        rooms[bestRoom].taken = True
                        if j.professor != "Staff":
                            professors.append(j.professor)
                        # add course and room to solution list for monday and wednesday (added as dictionary)
                        schedule.solution[1].append(j)
                        schedule.solution[3].append(j)

        # loop over all rooms and reset taken value for next time slot
        for t in rooms:
            # if a room is not taken at a certain time save it for alternatives
            if not t.taken:
                schedule.freeSlots.append({i: t})
            else:
                t.taken = False

    # add any unscheduled courses to correct list
    for i in courses:
        if not i.shed:
            schedule.unScheduled.append(i)

    # generate alternatives
    generate_alternatives(schedule, rooms, buildings, subjectToBuilding)

    return


# generate_alternatives: finds unscheduled courses the three best alternative times
# Input: A Schedule object
# Output: None
def generate_alternatives(schedule, rooms, buildings, subjectToBuilding):
    # smaller version of loop used in generate schedule except finding 3 of the best alternatives
    for i in schedule.freeSlots:
        for j in schedule.unScheduled:
            weights = calculateRoomWeights(j, rooms, {}, subjectToBuilding, 500, "warning.txt", buildings)
            bestAlt = weights.index(max(weights))
            w = max(weights)
            temp = list(weights)
            while len(j.alt) != 3:
                for k in i:
                    if rooms[bestAlt] == i[k]:
                        if i in j.alt:
                            break
                        j.alt.append(i)
                del temp[temp.index(max(temp))]
                if len(temp) == 0:
                    break
                w = max(temp)
                if w <= 0:
                    break
                bestAlt = weights.index(max(temp))

    return


# generate_output: creates an xlsx output file that contains the information of the scheduled and unscheduled classes
# Input: A Schedule object, a list of Course objects
# Output: None
def generate_output(schedule, courses, outF):
    # making a list that formats output info
    output_list = []
    Sheader = ["Course", "Title", "Version", "Section", "Professor", "Capacity", "Days", "Time", "Room", "Status"]
    output_list.append(Sheader)
    alt_list = []
    Aheader = ["course", "alt1", "alt2", "alt3"]
    alt_list.append(Aheader)

    # save scheduled courses as strings
    for solution in schedule.solution:
        for every in solution:
            if str(every.ver) == 'nan':
                version = ""
            else:
                version = every.ver
            temp = [every.subject + " " + str(every.course), every.title, version, every.sec, every.professor,
                    every.cap, every.days, str(every.Mtime), str(every.room), "scheduled"]
            if temp not in output_list:
                output_list.append(temp)

    # adding unscheduled courses to the output and alt info list as strings
    for i in courses:
        if not i.shed:
            temp = [i.subject + " " + str(i.course), i.title, version, i.sec, i.professor, i.cap, "", "", "", "unscheduled"]
            if temp not in output_list:
                output_list.append(temp)
            alt1_list = [(str(k), str(v)) for k, v in i.alt[0].items()]
            alt2_list = [(str(k), str(v)) for k, v in i.alt[1].items()]
            alt3_list = [(str(k), str(v)) for k, v in i.alt[2].items()]
            alt1 = " in ".join(alt1_list[0])
            alt2 = " in ".join(alt2_list[0])
            alt3 = " in ".join(alt3_list[0])

            temp = [i.subject + " " + str(i.course) + "; " + i.title + "; " + str(i.sec) + "; " + i.professor,
                    alt1, alt2, alt3]
            alt_list.append(temp)

    # writing to output excel workbook file that the user specifies as the second argument
    out_workbook = xlsxwriter.Workbook(outF)
    # create sheet and header schedule
    scheduleSheet = out_workbook.add_worksheet('Schedule')

    # add schedule
    for i in range(len(output_list)):
        for j in range(len(output_list[i])):
            scheduleSheet.write(i, j, output_list[i][j])

    # create alternatives sheet
    altSheet = out_workbook.add_worksheet('Alternatives')

    # add alternatives
    for i in range(len(alt_list)):
        for j in range(len(alt_list[i])):
            altSheet.write(i, j, alt_list[i][j])

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


def convert_Time(temp):
    if len(temp[1]) <= 2:
        hour = int(temp[1])
        if 1 <= hour <= 8:
            hour += 12
        minutes = 0
        return datetime.time(hour, minutes)
    elif len(temp[1]) == 4:
        hour = int(temp[1][0] + temp[1][1])
        if 1 <= hour <= 8:
            hour += 12
        temp = temp[1][len(temp[1])-2:] 
        minutes = int(temp)
        return datetime.time(hour, minutes)
    else:
        hour = int(temp[1][0])
        if 1 <= hour <= 8:
            hour += 12
        temp = temp[1][len(temp[1])-2:]
        minutes = int(temp[1])
    return datetime.time(hour, minutes)


def calculateRoomWeights(course, rooms, professorToBuilding, subjectToBuilding, LARGESTDISTANCE, warningTxt, buildings):
    # Roomweight Formula Multipliers
    SUBJECTWEIGHTMUL = 1
    PROFWEIGHTMUL = 5

    roomWeights = [None] * len(rooms)
    i = 0
    if not (course.professor in professorToBuilding):
        fo = open(warningTxt, "a")
        fo.write(str(
            datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized professor \"" + course.professor + "\".\n")
        fo.close()

    if not (course.subject in subjectToBuilding):
        fo = open(warningTxt, "a")
        fo.write(str(
            datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized subject \"" + course.subject + "\".\n")
        fo.close()
    # loop and get weights
    for room in rooms:
        # can room hold course?
        if room.cap < course.cap:
            roomWeights[i] = -1
            i += 1
        else:
            # Get professor distance
            if course.professor in professorToBuilding:
                distFromProf = calculateBuildingDistance(professorToBuilding[course.professor], room.name, buildings)
            else:
                distFromProf = LARGESTDISTANCE

                # Get subject distance
            if course.subject in subjectToBuilding:
                distFromSubject = calculateBuildingDistance(subjectToBuilding[course.subject], room.name, buildings)

            else:
                distFromSubject = LARGESTDISTANCE

            # calculate weight based on distances
            # make distance negative (so large distance is worse) and shift up (so its positive)
            profWeight = -distFromProf + LARGESTDISTANCE
            subjectWeight = -distFromSubject + LARGESTDISTANCE

            # apply weight multipliers then add to get roomweight
            roomWeight = profWeight * PROFWEIGHTMUL + subjectWeight * SUBJECTWEIGHTMUL
            roomWeights[i] = roomWeight
            i += 1

    return roomWeights


def calculateBuildingDistance(buildingName, roomName, buildings):
    # find buildings and lat and long
    for building in buildings:
        if buildingName in building.name:
            lat1 = building.lat
            lon1 = building.long
        if building.name in roomName:
            lat2 = building.lat
            lon2 = building.long

    # if both buildings the same return distance 0
    if lat1 == lat2 and lon1 == lon2:
        return 0

    # calculate distance between 2 buildings and return value
    location1 = (lat1, lon1)
    location2 = (lat2, lon2)
    distance = geodesic(location1, location2).meters

    return distance


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
