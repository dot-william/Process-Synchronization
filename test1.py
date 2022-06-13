import threading
from threading import Thread, Semaphore
import time
import random

# global semaphores
fittingRoom = Semaphore()
mutex = Semaphore()
# global color variable
gcolor = 'Green'
numSlots = 0
runningThreads = 0
finishedThreads = 0
firstPrinted = False

# get input from user
def askInput():
    invalidInput = True
    while(invalidInput):
        numSlots = input("Enter the number of slots inside the fitting room: ")
        numBlueThreads = input("Enter the number of blue threads: ")
        numGreenThreads = input("Enter the number of green threads: ")
        if int(numSlots) <= 0 or int(numBlueThreads) < 0 or int(numGreenThreads) < 0:
            print("Invalid inputs, try again.")
        else:
            invalidInput = False
    return numSlots, numBlueThreads, numGreenThreads

# create threads of the specified count and color and
def createThreads(queue, numThreads, color):
    for _ in range(numThreads):
        t = ColoredThread(color=color)
        queue.append(t)

# print all ColoredThreads in a list queue
def printQueue(queue):
    for t in queue:
        t.printSelf()
    print()

# ColoredThread object inherited from Thread to have color and id attributes
class ColoredThread(Thread):
    # method that will run when ColoredThread is started
    def run(self):
        global fittingRoom, mutex, gcolor, numSlots, runningThreads, finishedThreads, firstPrinted

        # acquire fitting room only if the global color matches self color
        fittingRoom.acquire()
        while (self.color != gcolor):
            fittingRoom.release()
            fittingRoom.acquire()

        # print message if a thread is the first to enter the fitting room
        if (runningThreads == 0 and not firstPrinted):
            firstPrinted = True
            print(f"{self.color} only")
        runningThreads += 1
        # run the critical section
        mutex.acquire()
        print("Running")
        time.sleep(0.1)
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
    global fittingRoom, mutex, gcolor, numSlots, runningThreads, finishedThreads, firstPrinted
    #Ask user input
    inputs = askInput()
    # test cases
    # inputs = (2, 3, 4)
    # inputs = (2, 4, 3)
    # inputs = (3, 7, 7) # odd blues and odd greens
    # inputs = (4, 8, 10) # even blues and even greens
    # inputs = (5, 7, 6) # odd blues, even greens
    # inputs = (3, 12, 9) # even blues, odd greens
    # inputs = (20, 5, 16) # total no. threads less than total slots
    # inputs = (10, 50, 50) # total no. threads less than total slots
    # inputs = (2, 4, 10)
    numSlots = int(inputs[0])
    numBlue = int(inputs[1])
    numGreen = int(inputs[2])
    runningThreads = 0
    print(f"slots = {numSlots}, blue = {numBlue}, green = {numGreen}\n")

    # initialize semaphores
    fittingRoom = Semaphore(numSlots)
    mutex = Semaphore()

    # Create green and blue threads
    queue = []
    createThreads(queue, numBlue, 'Blue')
    createThreads(queue, numGreen, 'Green')

    # Shuffle the ColoredThreads in the queue
    random.shuffle(queue)

    # assign ColoredThread IDs
    id=1
    for t in queue:
        t.setID(id)
        id += 1

    for t in queue:
        t.start()

    total = numGreen + numBlue

    while (total > 0):
        mutex.acquire()
        # if all the threads in the fitting room have finished executing
        
        if (runningThreads > 0 and runningThreads == finishedThreads):
            # decrement the total thread count
            if gcolor == 'Blue':
                numBlue -= runningThreads
            else:
                numGreen -= runningThreads
            total = numGreen + numBlue
            # reset finished threads count
            finishedThreads = 0
            # releases all occupied rooms in the fitting room
            print('Fitting room empty\n')
            while (runningThreads > 0):
                fittingRoom.release()
                runningThreads -= 1
            firstPrinted = False
            # changes the color that the fitting room accepts
            if gcolor == 'Blue' and numGreen > 0:
                gcolor = 'Green'
            elif numBlue > 0:
                gcolor = 'Blue'
        mutex.release()

if __name__ == "__main__":
    main()
