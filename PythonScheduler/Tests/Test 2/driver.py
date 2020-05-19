import schedule2
from schedule2 import *


try:
	dataClasses = pd.read_excel(r'ClassRoomTest2.xlsx', sheet_name='Schedule')  # reading file
except Exception:
	print("Error: There is no table in your classroom file titled 'Schedule'.")
try:
	dataRooms = pd.read_excel(r'ClassRoomTest2.xlsx', sheet_name='Capacity')  # reading file
except Exception:
	print("Error: There is no table in your classroom file titled 'Capacity'.")
try:
	dataBuild = pd.read_excel(r'ClassRoomTest2.xlsx', sheet_name='Coords')  # reading file
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
print_schedule(spring2020)
