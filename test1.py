import threading
from threading import Thread, Semaphore
import time
import random

'''
fittingRoom semaphore is a sign that there is still a vacant slot in the fitting room.
Nonzero if there is still a vacant slot, zero if there is no more vacant slot.

mutex ensures that only one thread can enter or leave the fitting room at a time.
'''

# global semaphores
fittingRoom = Semaphore()
mutex = Semaphore()
# global color variable
gcolor = 'Green'
numSlots = 0
runningThreads = 0
finishedThreads = 0

# get input from user
def askInput():
    numSlots = input("Enter the number of slots inside the fitting room: ")
    numBlueThreads = input("Enter the number of blue threads: ")
    numGreenThreads = input("Enter the number of green threads: ")
    return numSlots, numBlueThreads, numGreenThreads

# create threads of the specified count and color and
def createThreads(queue, numThreads, color):
    for _ in range(numThreads):
        t = ColoredThread(color=color)
        queue.append(t)

def printQueue(queue):
    for t in queue:
        t.printSelf()
    print()

class ColoredThread(Thread):

    def run(self):
        global fittingRoom, mutex, gcolor, numSlots, runningThreads, finishedThreads
        while(self.color != gcolor):
            pass
        if (self.color == gcolor):
            fittingRoom.acquire()
            if (runningThreads == 0):
                print(f"{self.color} only")
            runningThreads += 1
            mutex.acquire()
            print("Running")
            time.sleep(1)
            # print thread
            self.printSelf()
            mutex.release()
            finishedThreads += 1;


    def __init__(self, color):
        Thread.__init__(self, target=self.run)
        self.color = color
        self.id = -1

    def setID(self, id):
        self.id = id

    def printSelf(self):
        print(f"color = {self.color}, ID = {self.id}")

def main():
    global fittingRoom, mutex, gcolor, numSlots, runningThreads, finishedThreads
    #Ask user input
    # inputs = askInput()
    inputs = (2, 3, 4)
    numSlots = int(inputs[0])
    numBlue = int(inputs[1])
    numGreen = int(inputs[2])
    runningThreads = 0

    # initialize semaphores
    fittingRoom = Semaphore(numSlots)
    mutex = Semaphore()

    # Create green and blue threads
    queue = []
    createThreads(queue, numBlue, 'Blue')
    createThreads(queue, numGreen, 'Green')

    printQueue(queue)

    # Shuffle the elements
    random.shuffle(queue)

    # assign thread IDs
    id=1
    for t in queue:
        t.setID(id)
        id += 1

    printQueue(queue)

    for t in queue:
        t.start()

    while (True):
        if (runningThreads > 0 and runningThreads == finishedThreads):
            print(runningThreads)
            finishedThreads = 0
            mutex.acquire()
            while (runningThreads > 0):
                fittingRoom.release()
                runningThreads -= 1
            if gcolor == 'Blue':
                gcolor = 'Green';
            else:
                gcolor = 'Blue';
            print('Fitting room empty')
            mutex.release()

if __name__ == "__main__":
    main()
