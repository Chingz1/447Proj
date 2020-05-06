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
        distFromProf = calculateBuildingDistance(professorToBuilding[course.professor], room.name)        
    else :
        distFromProf = LARGESTDISTANCE                                                                  
        
    #Get subject distance
    if course.subject in subjectToBuilding:                                                       
        distFromSubject = calculateBuildingDistance(subjectToBuilding[course.subject], room.name)         
        
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
def calculateRoomWeights(course, rooms, professorToBuilding, subjectToBuilding, LARGESTDISTANCE, warningTxt):
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
            distFromProf = calculateBuildingDistance(professorToBuilding[course.professor], room.name)        
        else :
            distFromProf = LARGESTDISTANCE                                                                  
        
        #Get subject distance
        if course.subject in subjectToBuilding:                                                       
            distFromSubject = calculateBuildingDistance(subjectToBuilding[course.subject], room.name)         
        
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
def calculateBuildingDistance (buildingName, roomName):
    if (buildingName in roomName):
        return 5
    else:
        return 350
