import threading
from threading import Thread, Semaphore
import time
import random

fittingRoom = None
currentColor = None
id = 1
timeUnit = 0
currNumInRoom  = None
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
        t = threading.Thread(target=semaphoreTest, args=(color, id,))
        id+=1
        t.start()
        queue.append(t)
# def printSection(id, color):
#     global currNumInRoom
#     print(f"Thread ID = {id}, color = {color}")
#     time.sleep(3)
#     currNumInRoom-=1
    
def semaphoreTest(color,id):
    global fittingRoom

    fittingRoom.acquire()
    print(f"Thread ID = {id}, color = {color}\n", end="")
    fittingRoom.release()

def executeThread(color, id):
    global fittingRoom, currentColor, currNumInRoom, timeUnit

    # If no color yet is assigned
    if currentColor == None and currNumInRoom == 0:
        timeUnit += 1
        fittingRoom.acquire()
        currNumInRoom += 1
        print("---- Blue Only ----")
        print(f"\n----{id} was granted access! [currNum = {currNumInRoom}] @ {timeUnit}s----\n", end="")
        currentColor = color
        # printSection(id, color)
        print(f"Thread ID = {id}, color = {color}\n", end="")
        time.sleep(3)
        currNumInRoom-=1
        print(f"---->  {id} is releasing! [currNum = {currNumInRoom}]\n", end="")
        fittingRoom.release()

    # If color inside the fitting room is the same color
    elif currentColor == color:
        timeUnit += 1
        print(f"[Thread ID = {id}, color = {color} is trying to access] @ [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        fittingRoom.acquire()
        currNumInRoom += 1
        print(f"\n----{id} was granted access! [currNum = {currNumInRoom}]----@ {timeUnit}s\n", end="")
        # printSection(id, color)
        print(f"Thread ID = {id}, color = {color}\n", end="")
        time.sleep(3)
        currNumInRoom-=1
        print(f"---->  {id} is releasing! [currNum = {currNumInRoom}] @ {timeUnit}s\n", end="")
        fittingRoom.release()
    
    if currNumInRoom == 0:
        timeUnit += 1
        print(f">> Empty Fitting Room @ {timeUnit}s\n", end="")

def main():
    global fittingRoom, currNumInRoom 
    #Ask user input
    # inputs = askInput()
    inputs = (3, 10, 10)
    numSlots = int(inputs[0])
    numBlue = int(inputs[1])
    numGreen = int(inputs[2])
    threads = []
    fittingRoom = Semaphore(numSlots)
    currNumInRoom = 0
    createThreads(threads, numBlue, 'Blue')
    createThreads(threads, numGreen, 'Green')
    # for thread in threads:
    #     thread.join()


if __name__ == "__main__":
    main()



