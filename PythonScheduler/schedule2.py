import pandas as pd
import xlrd


class Course(object):
    shed = False

    def __init__(self, subject, course, title, ver, sec, professor, time, cap):
        self.subject = subject
        self.course = course
        self.title = title
        self.ver = ver
        self.sec = sec
        self.professor = professor
        self.time = time
        self.cap = cap

    def __repr__(self):
        return self.subject + " " + str(self.course) + " " + self.professor + " " + str(self.cap) + " " + self.time


class Room(object):
    taken = False

    def __init__(self, name, cap):
        self.name = name
        self.cap = cap

    def __repr__(self):
        return self.name


class Schedule(object):
    mw = []
    tt = []
    mwf = []

    solution = [[], [], [], [], []]


file = "ClassRoom.xlsx"
dataClasses = pd.read_excel(file, sheet_name='Schedule')  # reading file
dataRooms = pd.read_excel(file, sheet_name='Capacity')  # reading file

courses = dataClasses.values
rooms = dataRooms.values

courseList = []
roomList = []

spring2020 = Schedule()

for i in dataClasses.Time:
    if ("mw" in i) and not (i in spring2020.mw):
        spring2020.mw.append(i)
    if ("tt" in i) and not (i in spring2020.tt):
        spring2020.tt.append(i)
    if ("MWF" in i) and not (i in spring2020.mwf):
        spring2020.mwf.append(i)

for i in courses:
    courseList.append(Course(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

for i in rooms:
    roomList.append(Room(i[0], i[1]))


roomList.sort(key = lambda room: room.cap)

for i in spring2020.mw:
    for j in courseList:
        if (j.time == i) or ("MWF" in j.time):
            for k in roomList:
                if (j.cap <= k.cap) and not (k.taken) and not (j.shed):
                    j.shed = True
                    k.taken = True
                    spring2020.solution[0].append({j: k})
                    spring2020.solution[2].append({j: k})
                    if ("MWF" in j.time):
                        spring2020.solution[4].append({j: k})
    for t in roomList:
        t.taken = False

for i in spring2020.tt:
    for j in courseList:
        if j.time == i:
            for k in roomList:
                if (j.cap <= k.cap) and not (k.taken) and not (j.shed):
                    j.shed = True
                    k.taken = True
                    spring2020.solution[1].append({j: k})
                    spring2020.solution[3].append({j: k})
    for t in roomList:
        t.taken = False

print("Monday:")
for i in spring2020.solution[0]:
    print(i)

print("Tuesday:")
for i in spring2020.solution[1]:
    print(i)

print("Wednesday:")
for i in spring2020.solution[2]:
    print(i)

print("Thursday:")
for i in spring2020.solution[3]:
    print(i)

print("Friday:")
for i in spring2020.solution[4]:
    print(i)

print("Unscheduled:")
for i in courseList:
    if (not (i.shed)):
        print(i)

