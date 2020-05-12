#Calculate how much a class would like to be in a room, quantified as a roomweight.
#minimum roomWeight is zero, maximum is some positive value. -1 means class can't fit in room.

#Inputs:
#course - a standard course object
#room - a standard room object 
#professorToBuilding - a dictionary that uses professor string names as a key and building string names as a value.
#subjectToBuilding - a dictionary that uses subject string names as a key and building string names as a value. 
#LARGESTDISTANCE - the largest distance between buildings EX: 500
#warningTxt - the name of a file that the function writes to if a professor or subject are not keys to the subjectToBuilding and professorToBuilding dictionarys. EX: "warning.txt"

#Outputs:
#returns roomWeight, ideally an int (though idk cause python doesnt have types lmao). -1 if invalid room capacity.
import datetime
from geopy.distance import geodesic
def calculateRoomWeight(course, room, buildings, professorToBuilding, subjectToBuilding, LARGESTDISTANCE, warningTxt):
    #Roomweight Formula Multipliers
    SUBJECTWEIGHTMUL = 1
    PROFWEIGHTMUL = 5
    #Do we recognize professor or subject?
    if not(course.professor in professorToBuilding):                                                                                                                 
        fo = open(warningTxt, "a")
        fo.write(str(datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized professor \"" + course.professor + "\".\n")
        fo.close()

    if not(course.subject in subjectToBuilding):                                                                                                                                                                        
        fo = open(warningTxt, "a")
        fo.write(str(datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized subject \"" + course.subject + "\".\n")
        fo.close()
    #can room hold course?
    if (room.cap < course.cap) :                                                                        
        return -1
    
    #Get professor distance
    if course.professor in professorToBuilding:                                                  
        distFromProf = calculateBuildingDistance(professorToBuilding[course.professor], room.name, buildings)        
    else :
        distFromProf = LARGESTDISTANCE                                                                  
        
    #Get subject distance
    if course.subject in subjectToBuilding:                                                       
        distFromSubject = calculateBuildingDistance(subjectToBuilding[course.subject], room.name, buildings)         
        
    else:                                                                                                           
        distFromSubject = LARGESTDISTANCE
        
    #calculate weight based on distances
    #make distance negative (so large distance is worse) and shift up (so its positive)
    profWeight = -distFromProf + LARGESTDISTANCE                                                                                                                           
    subjectWeight = -distFromSubject + LARGESTDISTANCE
    
    #apply weight multipliers then add to get roomweight
    roomWeight = profWeight * PROFWEIGHTMUL + subjectWeight * SUBJECTWEIGHTMUL                         
    return roomWeight
####################### end of function



#same thing but works with a list of rooms and returns a list of weights
def calculateRoomWeights(course, rooms, buildings, professorToBuilding, subjectToBuilding, LARGESTDISTANCE, warningTxt):
    #Roomweight Formula Multipliers
    SUBJECTWEIGHTMUL = 1 
    PROFWEIGHTMUL = 5

    roomWeights = [None] * len(rooms)
    i = 0
    if not(course.professor in professorToBuilding):                                                                                                                 
        fo = open(warningTxt, "a")
        fo.write(str(datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized professor \"" + course.professor + "\".\n")
        fo.close()

    if not(course.subject in subjectToBuilding):                                                                                                                                                                        
        fo = open(warningTxt, "a")
        fo.write(str(datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized subject \"" + course.subject + "\".\n")
        fo.close()
    #loop and get weights
    for room in rooms :                                                                          
        #can room hold course?
        if (room.cap < course.cap) :                                                                          
            roomWeights[i] = -1
            i += 1
            continue
    
        #Get professor distance
        if course.professor in professorToBuilding:                                                  
            distFromProf = calculateBuildingDistance(professorToBuilding[course.professor], room.name, buildings)        
        else :
            distFromProf = LARGESTDISTANCE                                                                  
        
        #Get subject distance
        if course.subject in subjectToBuilding:                                                       
            distFromSubject = calculateBuildingDistance(subjectToBuilding[course.subject], room.name, buildings)         
        
        else:                                                                                                            
            distFromSubject = LARGESTDISTANCE
        
        #calculate weight based on distances
        #make distance negative (so large distance is worse) and shift up (so its positive)
        profWeight = -distFromProf + LARGESTDISTANCE                                                                                                                            
        subjectWeight = -distFromSubject + LARGESTDISTANCE
        
        #apply weight multipliers then add to get roomweight  
        roomWeight = profWeight * PROFWEIGHTMUL + subjectWeight * SUBJECTWEIGHTMUL                          
        roomWeights[i] = roomWeight
        i += 1

    return roomWeights                                                                                         
#################### end of function

#Just an example i used for testing. Real calculateBuildingDistance should get actual distances.
def calculateBuildingDistance (buildingName, roomName, buildings):
    for building in buildings:
        if buildingName in building.name:
            lat1 = building.lat
            lon1 = building.long
        if building.name in roomName:
            lat2 = building.lat
            lon2 = building.long
    if (lat1 == lat2 and lon1 == lon2):
        return 0
    location1 = (lat1, lon1)
    location2 = (lat2, lon2)
    distance = geodesic(location1, location2).meters
    print(distance)
    return distance
#################### end of function    

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
#building object
class Building(object):
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

    def __repr__(self):
        return self.name + " lat = " + str(self.lat) + "lang = " + str(self.long)

    def __str__(self):
        return self.name + " lat = " + str(self.lat) + "lang = " + str(self.long)



warningFile = "warning.txt"
exampleCourse1 = Course("cmsc", "course1", "title1", "ver", "sec", "professor1", "time", 10)
exampleCourse2 = Course("cmpe", "course2", "title2", "ver", "sec", "professor2", "time", 10)
exampleRoom1 = Room("building1 101", 20)
exampleRoom2 = Room("building2 102", 10)
building1 = Building("building1", 39.253902, -76.710881)
building2 = Building("building2", 39.254564, -76.714027)
buildingList = [building1, building2]
professorToBuilding = {"professor1" : "building1" , "professor2" : "building2"}
subjectToBuilding = {"cmsc" : "building1"}
LARGESTDISTANCE = 500
warningTextFile = "warning.txt"
rooms = [exampleRoom1, exampleRoom2]
print(calculateRoomWeights(exampleCourse2 , rooms , buildingList, professorToBuilding, subjectToBuilding, LARGESTDISTANCE, warningTextFile))
