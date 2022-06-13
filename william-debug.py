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
numAllowed = None

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
        time.sleep(1)
        queue.append(t)
        
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

def switchColor():
    global currentColorTotal, counter, counter
    currentColorTotal = findCurrentColorTotal(currentColor) # gets total threads of the current color
    
    if counter != 0 and counter == currentColorTotal // 2:
        numExecuted = counter
        setCurrentColorTotal(numExecuted)
        print(f"Switching colors!!! Count after execution: {currentColorTotal}\n", end="")
        alternateColor()
        print(f"After color change: {currentColor}\n", end="")
        counter = 0

def execute(id):
    global counter, currNumInRoom, currentColor

    print(f"\nT{id} was granted access!\n", end="")
    currNumInRoom += 1 # thread enters room
    # print(f"Current {currentColor} total initialized: {currentColorTotal}\n", end="")
    print(f"Thread ID = {id}, color = {currentColor}\n", end="")
    time.sleep(10) # stays in the room for this amount of time
    print(f"T{id} is about to release! [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")

# def executeThread(color, id):
#     global fittingRoom, currentColor, currNumInRoom, timeUnit, currentColorTotal
#     global counter
#     global enterRoom

#     # If no color is assigned yet and no one is in the room - initialize
#     if currentColor == None and currNumInRoom == 0:
#         print(f"T{id} is trying to access from first if statement! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
#         fittingRoom.acquire()
#         print(f"\nT{id} was granted access!\n", end="")
#         currentColor = color # assign Color
#         currentColorTotal = findCurrentColorTotal(currentColor) # get current total of current color
#         execute()
#         fittingRoom.release()
#         print(f"T{id} is released. [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
#         currNumInRoom -= 1

#     # Check current color if matched and if the counter of number executed threads hasn't reached the half
#     elif currentColor == color and counter < currentTotal // 2 :
#         print(f"T{id} is trying to access! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
#         fittingRoom.acquire()
#         print(f"\nT{id} was granted access! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
#         counter += 1 # increase counter of thread that acquired resource
#         currNumInRoom += 1 # thread enters room
        
#         # print(f"Thread ID = {id}, color = {color}\n", end="")
#         time.sleep(10)
#         print(f"T{id} is about to release! [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
#         fittingRoom.release()
#         currNumInRoom-=1
#         print(f"T{id} is released. [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")

#     # if counter reached the half of the current total
#     elif counter >=    // 2:
#         enterRoom = False

#     # If only one process is left
#     elif currentColor == color and currentTotal == 1:
#         print(f"T{id} is trying to access! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
#         fittingRoom.acquire()
#         currNumInRoom += 1
#         print(f"\nT{id} was granted access! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
#         time.sleep(10)
#         print(f"T{id} is about to release! [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
#         fittingRoom.release()
#         currNumInRoom-=1
#         print(f"T{id} is released. [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")

#     # if the counter is greater than the half of the current color processing 

#     if currNumInRoom == 0:
#         timeUnit += 1
#         print(f">> Empty Fitting Room @ {timeUnit}s\n", end="")
#         if counter == currentColorTotal // 2:
#             checkIfSwitchColor()

def executeThread(color, id):
    global fittingRoom, currentColor, currNumInRoom, timeUnit, currentColorTotal
    global counter
    
    # For the very first thread
    if currentColor == None and currNumInRoom == 0:
        print(f"T{id} is trying to access from first if statement! @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        fittingRoom.acquire()
        counter += 1
        # increase counter of thread that acquired resource
        currentColor = color # assign Color
        currentColorTotal = findCurrentColorTotal(currentColor) # get current total of current color
        print(f"---- {currentColor} Only ----\n", end="")
        execute(id)
        fittingRoom.release()
        print(f"T{id} is released. [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        currNumInRoom -= 1
        notFinished = False # So thread can exit the loop

    # Where other threads go
    notFinished = True
    while(notFinished):        
        # The first thread to enter room after color switch
        if ((counter == 0 and currNumInRoom == 0) and color == currentColor) or findCurrentColorTotal(currentColor) == 0:
            print(f"T{id} is trying to access from first if statement! @ [currNum = {currNumInRoom}] @ {counter}\n", end="")
            fittingRoom.acquire()
            counter += 1 # increase counter of thread that acquired resource
            print(f"\nIn while if\n", end="")
            #currentColor = color # assign Color
            currentColorTotal = findCurrentColorTotal(currentColor) # get current total of current color
            print(f"---- {currentColor} Only ----\n", end="")
            execute(id)
            fittingRoom.release()
            print(f"T{id} is released. [currNum = {currNumInRoom}]\n", end="")
            currNumInRoom -= 1
            notFinished = False # So thread can exit the loop
            # if counter reaches the half of the total process and no more process are in the room OR there are no more processes left, switch color
            if ((counter >= currentColorTotal // 2) and currNumInRoom == 0) or (currentColorTotal // 2 == 0):
                switchColor()
        
        # The rest of threads - check current color if matched and if the counter of number executed threads hasn't reached the half
        elif currentColor == color and counter < currentColorTotal // 2:
            print(f"T{id} is trying to access! @ [currNum = {currNumInRoom}] and counter: {counter}\n", end="")
            fittingRoom.acquire()
            counter += 1 # increase counter of thread that acquired resource
            print(f"\nT{id} In while elif and counter: {counter}\n", end="")
            # print(f"Thread ID = {id}, color = {color}\n", end="")
            execute(id)
            fittingRoom.release()
            currNumInRoom-=1
            print(f"T{id} is released. [currNum = {currNumInRoom}]\n", end="")
            notFinished = False
            # if counter reaches the half of the total process and no more process are in the room OR there are no more processes left, switch color
            if ((counter >= currentColorTotal // 2) and currNumInRoom == 0) or (currentColorTotal // 2 == 0):
                switchColor()
        


def main():
    global fittingRoom, currNumInRoom, totalBlue, totalGreen, numAllowed
    #Ask user input
    # inputs = askInput()
    inputs = (3, 10, 10)
    numSlots = int(inputs[0])
    numBlue = int(inputs[1])
    numGreen = int(inputs[2])
    threads = []
    fittingRoom = Semaphore(numSlots)
    numAllowed = Semaphore(numSlots)
    currNumInRoom = 0
    totalBlue = numBlue
    totalGreen = numGreen
    createThreads(threads, numBlue, 'Blue')
    createThreads(threads, numGreen, 'Green')

if __name__ == "__main__":
    main()



