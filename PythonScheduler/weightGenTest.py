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
def calculateRoomWeight(course, room, professorToBuilding, subjectToBuilding, LARGESTDISTANCE, warningTxt):
    #Roomweight Formula Multipliers
    SUBJECTWEIGHTMUL = 1
    PROFWEIGHTMUL = 5
    #can room hold course?
    if (room.cap < course.cap) :                                                                        
        return -1
    
    #Get professor distance
    if course.professor in professorToBuilding:                                                  
        distFromProf = calculateBuildingDistance(professorToBuilding[course.professor], room.building)        
    else :
        distFromProf = LARGESTDISTANCE                                                                  
        fo = open(warningTxt, "a")
        fo.write(str(datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized professor \"" + course.professor + "\".\n")
        fo.close()
        
    #Get subject distance
    if course.subject in subjectToBuilding:                                                       
        distFromSubject = calculateBuildingDistance(subjectToBuilding[course.subject], room.building)         
        
    else:                                                                                                           
        distFromSubject = LARGESTDISTANCE
        fo = open(warningTxt, "a")
        fo.write(str(datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized subject \"" + course.subject + "\".\n")
        fo.close()
        
    #calculate weight based on distances
    #make distance negative (so large distance is worse) and shift up (so its positive)
    profWeight = -distFromProf + LARGESTDISTANCE                                                                                                                           
    subjectWeight = -distFromSubject + LARGESTDISTANCE
    
    #apply weight multipliers then add to get roomweight
    roomWeight = profWeight * PROFWEIGHTMUL + subjectWeight * SUBJECTWEIGHTMUL                         
    return roomWeight
####################### end of function



#same thing but works with a list of rooms and returns a list of weights
def calculateRoomWeights(course, rooms, professorToBuilding, subjectToBuilding, LARGESTDISTANCE, warningTxt):
    #Roomweight Formula Multipliers
    SUBJECTWEIGHTMUL = 1 
    PROFWEIGHTMUL = 5

    roomWeights = [None] * len(rooms)
    i = 0
    
    #loop and get weights
    for room in rooms :                                                                          
        #can room hold course?
        if (room.cap < course.cap) :                                                                          
            roomWeights[i] = -1
            i += 1
            continue
    
        #Get professor distance
        if course.professor in professorToBuilding:                                                  
            distFromProf = calculateBuildingDistance(professorToBuilding[course.professor], room.building)        
        else :
            distFromProf = LARGESTDISTANCE                                                                  
            fo = open(warningTxt, "a")
            fo.write(str(datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized professor \"" + course.professor + "\".\n")
            fo.close()
        
        #Get subject distance
        if course.subject in subjectToBuilding:                                                       
            distFromSubject = calculateBuildingDistance(subjectToBuilding[course.subject], room.building)         
        
        else:                                                                                                            
            distFromSubject = LARGESTDISTANCE
            fo = open(warningTxt, "a")
            fo.write(str(datetime.datetime.now()) + " The course \"" + course.title + "\" has unrecognized subject \"" + course.subject + "\".\n")
            fo.close()
        
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
    def __init__(self, name, cap, building):
        self.name = name
        self.cap = cap
        self.building = building

    # room object print format
    def __repr__(self):
        return self.name

def calculateBuildingDistance (buildingName1, buildingName2):
    if (buildingName1 == buildingName2):
        return 100
    else:
        return 350


warningFile = "warning.txt"
exampleCourse1 = Course("cmsc", "course1", "title", "ver", "sec", "professor1", "time", 10)
exampleCourse2 = Course("cmpe", "course2", "title", "ver", "sec", "professor2", "time", 10)
exampleRoom1 = Room("room1", 20, "building1")
exampleRoom2 = Room("room2", 10, "building2")
professorToBuilding = {"professor1" : "building1" , "professor2" : "building2"}
subjectToBuilding = {"cmsc" : "building1"}
LARGESTDISTANCE = 500
warningTextFile = "warning.txt"
rooms = [exampleRoom1, exampleRoom2]
print(calculateRoomWeights(exampleCourse1 , rooms , professorToBuilding, subjectToBuilding, LARGESTDISTANCE, warningTextFile))
