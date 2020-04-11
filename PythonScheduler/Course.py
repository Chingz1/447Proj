from constraint import *
import pandas as pd


class Course(object):

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
        return self.subject + str(self.course)


class Room:
    def __init__(self, name, cap):
        self.name = name
        self.cap = cap

    def __repr__(self):
        return self.name


file = "ClassRoom.xlsx"
dataClasses = pd.read_excel(file, sheet_name='Schedule')  # reading file
dataRooms = pd.read_excel(file, sheet_name='Capacity')  # reading file

courses = dataClasses.values
rooms = dataRooms.values
courseList = []
roomList = []

for i in courses:
    courseList.append(Course(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

for i in rooms:
    roomList.append(Room(i[0], i[1]))

# create Dict
database = {'courses': courseList, 'rooms': roomList}

problem = Problem()

for key, value in database.items():
    problem.addVariable(key, value)


def cap_constraint(Course, Room):
    if (Course.cap <= Room.cap):
        return True


problem.addConstraint(cap_constraint, ['courses', 'rooms'])

# Get solutions
solutions = problem.getSolutions()
print(len(solutions))
print(*solutions, sep = "\n") 
