import sys
import random
import math 
import copy
import time

#test comment
def getOptimalIndex(target,list):
    if len(list)<=0:
        return -1,0
    midpoint= math.floor(len(list)/2)
    if list[midpoint] == target:
        return midpoint, 0
    dif = list[midpoint]-target
    if dif>0:
        tList=list[0:midpoint]
        childIndex,childDif = getOptimalIndex(target,tList)
        if childIndex>=0 and abs(childDif)<dif:
            return childIndex,childDif
        return midpoint, dif
    else:
        tList=list[midpoint+1:len(list)]
        childIndex,childDif = getOptimalIndex(target,tList)
        if abs(childDif)<abs(dif) and childIndex>=0:
            return childIndex+1+midpoint,childDif
    return midpoint,dif    

# This function is extremely unoptimal, but it was my first attempt.
def generate_group1(completeGroups,currentGroup,remainingValues):
    global successCount
    global finalGroups
    loopLen=len(remainingValues)
    curLen=len(currentGroup)
    maxRemaining=sum(remainingValues[loopLen-(rating-curLen):loopLen])
    if curLen>0:
        maxRemaining+= sum(currentGroup)
    #check if there are enough high values left to complete at least 1 more group
    if loopLen==0 or maxRemaining<tn:
        # Not enough left, endpoint found
        tempSuccess= len(completeGroups)
        if tempSuccess>successCount:
            finalGroups = copy.deepcopy(completeGroups)
            successCount=tempSuccess
            if len(remainingValues)>0:
                finalGroups.append(currentGroup+remainingValues)
            #print(f"new best {successCount} {finalGroups}")
    else:
        #Atleast 1 group can still be made
        dif = tn - sum(currentGroup)
        for i in range(loopLen):
            #tIndex = startIndex+i
            tIndex=loopLen-1-i
            if tIndex>=loopLen:
                tIndex = tIndex-loopLen
            tempComplete = copy.deepcopy(completeGroups)
            tempGroup = copy.deepcopy(currentGroup)
            #print(f"adding index {tIndex} from list {remainingValues}")
            tempGroup.append(remainingValues[tIndex])
            tempRemaining=copy.deepcopy(remainingValues)
            del tempRemaining[tIndex]
            if sum(tempGroup)>= tn:
                tempComplete.append(tempGroup)
                tempGroup=[]
            generate_group1(tempComplete,tempGroup,tempRemaining)

def generate_group2(groupCount,remainingvalues): 
    finalGroups = []
    successCount = 0
    for i in range(groupCount):
        successTarget=groupCount-i
        tg=[]
        rm = copy.deepcopy(remainingvalues)
        for i in range(successTarget):
            tg.append([])
        result = generateSuccessGroups(tg,rm)
        if result:
            finalGroups = tg+rm
            successCount = successTarget
            break
    return successCount, finalGroups

def generateSuccessGroups(groups, remainingValues):
    loopLen = len(groups)
    for i in range(loopLen):
        groups[i].append(remainingValues[-1])
        del remainingValues[-1]
    for i in range(loopLen):
        while sum(groups[i])<tn:
            if len(groups[i])>=rating or len(remainingValues)==0:
                return False
            dif = tn-sum(groups[i])
            bestIndex,_ = getOptimalIndex(dif,remainingValues)
            groups[i].append(remainingValues[bestIndex])
            del remainingValues[bestIndex]
    return True

def rollDice(count, size, ordered):
    results=[]
    for i in range(count):
        results.append(random.randrange(1,size,1))
    if ordered:
        return sorted(results)
    return results

def getSuccesses(target, rating, diceList, diceSize):
    diceCount = tethers*rating
    maxSuccess = math.floor(diceCount/math.ceil(target/diceSize))
    successCount, successList = generate_group2(maxSuccess,diceList)
    return successCount, successList

args = sys.argv
if 1 < len(args):
    tethers = int(args[1])
    if 2 < len(args):
        rating = int(args[2])
        if 3 < len(args):
            tn = int(args[3])
            sortedList = rollDice(tethers*rating,6,True)
            starttime= time.time()
            successCount, finalGroups= getSuccesses(tn, rating, sortedList,6)
            print(f"execution time for Gen2: {time.time()-starttime} seconds")
            print(f"best result count {successCount} on {finalGroups}")


def TestRoll(tethers, rating, tn):
    sortedList = rollDice(tethers*rating,6,True)
    starttime= time.time()
    successCount, finalGroups= getSuccesses(tn, rating, sortedList,6)
    print(f"execution time for Gen2: {time.time()-starttime} seconds")
    print(f"best result count {successCount} on {finalGroups}")
