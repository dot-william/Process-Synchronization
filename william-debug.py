import threading
from threading import Thread, Semaphore
import time
import random

from gevent import Greenlet

fittingRoom = None # Semaphore
id = 1 # For Thread Id
timeUnit = 0 # delete this
currNumInRoom  = None # delete this later

currentColor = None  # keeps track current color allowed
currentColorTotal = 0

totalBlue = 0 
totalGreen = 0
counter = 0 # used to track if need to switch, increments whenever it goes in the section

# get input from user
def askInput():
    numSlots = input("Enter the number of slots inside the fitting room: ")
    numBlueThreads = input("Enter the number of blue threads: ")
    numGreenThreads = input("Enter the number of green threads: ")
    return numSlots, numBlueThreads, numGreenThreads


# create threads of the specified count and color and
def createThreads(queue, numThreads, color):
    global id
    for _ in range(numThreads):
        t = threading.Thread(target=executeThread, args=(color, id,))
        print(f"~~T{id} made")
        id+=1
        t.start()
        queue.append(t)
        #time.sleep(1)
        
# def printSection(id, color):
#     global currNumInRoom
#     print(f"Thread ID = {id}, color = {color}")
#     time.sleep(10)
    
def findCurrentColorTotal(color):
    global totalBlue, totalGreen
    if color == "Blue":
        total = totalBlue
    else:
        total = totalGreen
    return total

def setCurrentColorTotal(numExecuted):
    global currentColor, totalBlue, totalGreen

    if currentColor == "Blue":
        totalBlue = totalBlue - numExecuted
    else:
        totalGreen = totalGreen - numExecuted

def alternateColor():
    global currentColor
    print(f"Before color change: {currentColor}\n", end="")
    if currentColor == "Blue":
        currentColor = "Green"
    else:
        currentColor = "Blue"

def checkIfSwitchColor():
    global currentColorTotal, currentColor, counter

    currentColorTotal = findCurrentColorTotal(currentColor) # gets total threads of the current color
    
    if currentColor != None and counter == currentColorTotal // 2:
        numExecuted = counter
        setCurrentColorTotal(numExecuted)
        currentColorTotal = findCurrentColorTotal(currentColor)
        print(f"Switching colors count: {currentColor}\n", end="")
        alternateColor()
        print(f"After color change: {currentColor}\n", end="")
        counter = 0

def executeThread(color, id):
    global fittingRoom, currentColor, currNumInRoom, timeUnit
    global counter

    
    # If no color is assigned yet
    if currentColor == None and currNumInRoom == 0:
        print(f"T{id} is trying to access! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        fittingRoom.acquire()
        counter += 1 
        currNumInRoom += 1
        currentColor = color # assign Color
        currentTotal = findCurrentColorTotal(currentColor) # set current total
        print(f"----Current {currentColor} total initialized: {currentTotal}----\n", end="")
        print(f"---- {currentColor} Only ----\n", end="")
        print(f"\nT{id} was granted access!\n", end="")
        # printSection(id, color)
        # print(f"Thread ID = {id}, color = {color}\n", end="")
        time.sleep(10) # this is how long it executes/stays in the section
        print(f"T{id} is about to release! [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        fittingRoom.release()
        currNumInRoom -= 1
        print(f"T{id} is released. [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
    
    # If color inside the fitting room is the same color
    elif currentColor == color and counter < currentTotal // 2 :
        timeUnit += 1
        print(f"T{id} is trying to access! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        fittingRoom.acquire()
        counter += 1
        currNumInRoom += 1
        print(f"\nT{id} was granted access! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        # printSection(id, color)
        # print(f"Thread ID = {id}, color = {color}\n", end="")
        time.sleep(10)
        print(f"T{id} is about to release! [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        fittingRoom.release()
        currNumInRoom-=1
        print(f"T{id} is released. [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
    
    if currNumInRoom == 0:
        timeUnit += 1
        print(f">> Empty Fitting Room @ {timeUnit}s\n", end="")
        if counter == currentColorTotal // 2:
            checkIfSwitchColor()
    
    


def printQueue(queue):
    for t in queue:
        t.printSelf()
    print()


def main():
    global fittingRoom, currNumInRoom, totalBlue, totalGreen
    #Ask user input
    # inputs = askInput()
    inputs = (3, 10, 10)
    numSlots = int(inputs[0])
    numBlue = int(inputs[1])
    numGreen = int(inputs[2])
    threads = []
    fittingRoom = Semaphore(numSlots)
    currNumInRoom = 0
    totalBlue = numBlue
    totalGreen = numGreen
    createThreads(threads, numBlue, 'Blue')
    createThreads(threads, numGreen, 'Green')

if __name__ == "__main__":
    main()



