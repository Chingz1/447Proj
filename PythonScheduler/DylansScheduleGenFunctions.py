#takes in list of all course objects (course objects defined in the same way as they were)
#takes in list of all room objects (room objects defined in the same way as they were)
#takes in list of building objects (up to calculateBuildingDist how this works)
#takes in dictionary with subject string as key to its building (Don't have to create one for every subject, subjects not found in dictionary just get the distance set to max if subject not recognized)
#takes in dictionary with professor string as key to its building string (Don't have to create based on input, just create an empty one)
#validStartTimes are all times courses may start. May simply be a list of all unique times. Should be an integer value
#validDayPairs are all valid day pairs "MW", "TTh", "MWF" but may also be "MTWThF" in weird cases

#generates best possible room/course assignment between for all courses given rooms and building distances.
#returns classSchedule[cID] = [dpID, tID, rID] and invalidClasses, a list of class IDs that were invalid.
#ID's for courses and rooms are the index of the course and room in the list of courses/rooms obtained as input from the user.
#User input function or some other top level code may handle creating data sets needed by this function.
def scheduleGen(courses, rooms, buildings, subjectBuilding, professorBuilding, validStartTimes,validDayPairs):
    import math
    #Determine Best and Worst Building Distances
    BESTDIST = 0
    WORSTDIST = 0
    for building1 in buildings:
       for building2 in buildings:
           dist = calculateBuildingDistance(building1, building2)
           if (dist > WORSTDIST):
               WORSTDIST = dist

    #Determine WORSTROOMWEIGHT and BESTROOMWEIGHT based on the best and worst distances
    WORSTROOMWEIGHT = (-(WORSTDIST - BESTDIST))*SUBJECTDISTMUL + (-(WORSTDIST - BESTDIST))*PROFDISTMUL
    BESTROOMWEIGHT = 0
    #Determine range of roomweights
    ROOMWEIGHTRANGE = BESTROOMWEIGHT - WORSTROOMWEIGHT #ex roomweight may range from 0 to -700.


    
    #Calculate room weight for each class
    courseRoomWeights = [[]] #2d list of weights
    for cID in len(courses):
        for rID in len(rooms):
            courseRoomWeights[cID][rID] = calculateRoomWeight(courses[cID], rooms[rID], subjectBuilding, WORSTDIST)
    
            
    numDifferentSchedules = len(rooms) * len(validStartTimes) * len(validDayPairs)
    scheduleWeights[numDifferentSchedules]      #list of schedule weights for each schedule
    scheduleAlternatives[]                      #list of classes that were invalid for best schedule (used after best schedule is found)
    schedules = [[[[[]]]]]                      #5d list schedID, dpID, rID, tID, cID (may contain multiple course IDs for given day/room/time) useful for minimizing weights
    schedulesClass = [[[]]]                     #2d list schedule then class id returns array of that classes assigned day, time, and room. Useful for detecting courses overlapping at different times
    #initialize each schedule to 0 weight to start
    for schedID in numDifferentSchedules:
        scheduleWeights[schedID] = 0
                
    #generate weight/preferability for every course entering every possible schedule
    for cID in len(courses):
        for dpID in len(validDayPairs):
            for rID in len(rooms):
                for tID in len(validStartTimes):
                    schedID = dpID*len(validStartTimes)*len(rooms)+rID*len(validStartTimes)+tID
                    
                    scheduleWeights[schedID] += courseRoomWeights[cID][rID]
                    schedules[schedID][dpID][rID][tID].append(cID) #in hindsight this is less efficient to use than the schedulesClass so i may change parts that use this to only use schedulesClass.
                    schedulesClass[schedID][cID] = [dpID, tID, rID]
    
    #Calculate invalidWeights such that highest priority is a multiple of smaller ones times the number of classes that could raise that invalid weight.
    invalidTimeWeight = -(ROOMWEIGHTRANGE*len(courses)+1)
    invalidDayPairWeight = invalidTimeWeight * len(courses) - 1
    invalidCourseConflictWeight = invalidDayPairWeight * len(courses) - 1
    invalidRoomCapWeight = invalidCourseConflictWeight * len(courses) - 1

    #detect courses assigned to incorrect rooms, times, or days, update scheduleWeight as appropriate.
    for schedID in len(schedules):
        for cID in len(schedulesClass[schedID]):
            if (rooms[classSchedule[cID][2]].cap < courses[cID].cap):
                scheduleWeights[schedID] += invalidRoomCapWeight
            if (timeFromString(courses[cID1].time) != validStartTimes[classSchedule[cID1][1]]):
                scheduleWeights[schedID] += invalidTimeWeight
            if (dayPairFromString(courses[cID1].time) != validDayPairs[classSchedule[cID1][0]]):
                scheduleWeights[schedID] += invalidDayPairWeight
    
    #detect overlap between days two days and two courses, update schedule weights as appropriate
    for schedID in numDifferentSchedules:
         for cID1 in len(courses):
            for cID2 in len(courses):
                if (cID1 != cID2):
                    dpID1 = schedulesClass[schedID][cID1][0] 
                    dpID2 = schedulesClass[schedID][cID2][0]
                    tID1 = schedulesClass[schedID][cID1][1] 
                    tID2 = schedulesClass[schedID][cID2][1]
                    rID1 = schedulesClass[schedID][cID1][2] 
                    rID2 = schedulesClass[schedID][cID2][2]
                    if (  timeOverlap(validStartTimes[tID1], validStartTimes[tID2]) && rID1 == rID2 && dayPairsOverlap(validDayPairs[dpID1],validDayPairs[dpID2])  ):
                        scheduleWeights[schedID] += invalidCourseConflictWeight

                        
    #get best schedule                         
    bestScheduleWeight = min(ScheduleWeights) #returns minimum value in list
    bestScheduleIndex = index(bestScheduleWeight) #returns index of *first* value in list with best weight
    
    classSchedule = schedulesClass[bestScheduleIndex]
    invalidClasses[] #list of classIDs for invalid classes that will need alternatives
    overlapClasses[[]] #list of pairs of classes that overlap. Must find which combination to choose is best...

    #determine invalid classes
    for cID1 in len(classSchedule):
        if (rooms[classSchedule[cID1][2]].cap < courses[cID1].cap): #bad room capacity
            if (invalidClasses.count(cID1) == 0):
                invalidClasses.append(cID1)
        if (timeFromString(courses[cID1].time) != validStartTimes[classSchedule[cID1][1]]): #bad time
            if (invalidClasses.count(cID1) == 0):
                invalidClasses.append(cID1)
        if (dayPairFromString(courses[cID1].time) != validDayPairs[classSchedule[cID1][0]]): #bad day
            if (invalidClasses.count(cID1) == 0):
                invalidClasses.append(cID1)
    


    #determine overlapping classes, pick second one and term it invalid (technically could compare weights of two and invalidate course that has lower weight in a given conflict, should change it to that in future)
    for cID1 in len(classSchedule):               
        for cID2 in len(classSchedule):
            if (cID1 != cID2 && invalidClasses.count(cID1) == 0 && invalidClasses.count(cID2) == 0):
                dpID1 = schedulesClass[schedID][cID1][0] 
                dpID2 = schedulesClass[schedID][cID2][0]
                tID1 = schedulesClass[schedID][cID1][1]
                tID2 = schedulesClass[schedID][cID2][1]
                rID1 = schedulesClass[schedID][cID1][2] 
                rID2 = schedulesClass[schedID][cID2][2]
                if (  timeOverlap(validStartTimes[tID1], validStartTimes[tID2]) && rID1 == rID2 && dayPairsOverlap(validDayPairs[dpID1],validDayPairs[dpID2])  ): #day/time/room conflict for 2 courses
                    if (invalidClasses.count(cID2) == 0):
                        invalidClasses.append(cID2)

    return classSchedule, invalidClasses
###########################################################################End of Generate Schedule

#used by the scheduleGen function
def calculateRoomWeight(course, room, professorBuilding, subjectBuilding, WORSTDIST):
    #Roomweight Formula Multipliers
    SUBJECTDISTMUL = 1
    PROFDISTMUL = 5

    #professor distance
    if (has_key(professorBuilding, course.professor)):                                              #If we know the professors building, get distance from it
        distFromProf = calculateBuildingDistance(professorBuilding[course.professor], room.building)
    else :                                                                                          
        distFromProf = WORSTDIST                                                                    #else just use worst possible distance


    #subject distance
    if (has_key(subjectBuilding, course.subject):                                                   #if we know subjects central building, get distance from it
        distFromSubject = calculateBuildingDistance(subjectBuilding[course.subject], room.building)
    else:                                                                                             #else just use worst possible distance              
        distFromSubject = WORSTDIST

    #calculate weight based on distances
    roomWeight = (-distFromSubject) * SUBJECTDISTMUL + (-distFromProf) * PROFDISTMUL
    return roomWeight        
##############################################################################End of calculateRoomWeight
#Used by the scheduleGen function to return distance between two buildings given a string. May need more input...
def calculateBuildingDistance(buildingString1, buildingString2):
    #calculate distance however w longitude latitude etc
    
    return distance

#takes in a time string and returns start time in military time
def timeFromString(timeString):
    
    return time

#takes in a time string and returns the day pairing (MW, TTh, MWF, etc)
def dayPairFromString(timeString):

    return dayPair
#determines if two times overlap, by checking if their start times are within 90 minutes of each other.
def timeOverlap(timeVal1, timeVal2):
    
    return #true or false
#determines if a day string such as mwf overlaps with another daystring such as mw, but ideally can work for any day string?
def dayOverlap(daysStr1, daysStr2):
    
    return #true or false
