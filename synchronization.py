import threading
from threading import Thread, Semaphore
import time
import random

# global empty, full, and mutex semaphores
empty = Semaphore()
full = Semaphore()
mutex = Semaphore()
# global color variable
color = 'b'
# global decline variable
decline = False
# total processes count
total = 0

# get input from user
def askInput():
    numSlots = input("Enter the number of slots inside the fitting room: ")
    numBlueThreads = input("Enter the number of blue threads: ")
    numGreenThreads = input("Enter the number of green threads: ")
    return numSlots, numBlueThreads, numGreenThreads

# create threads of the specified count and color and
def createThreads(queue, numThreads, color):
    for _ in range(numThreads):
        t = ColoredThread(target=run, color=color)
        queue.append(t)

def printQueue(queue):
    for t in queue:
        t.printSelf()
    print()

class ColoredThread(Thread):
    global empty, full, mutex, color, decline, total

    def __init__(self, target, color):
        Thread.__init__(self, target=run)
        self.color = color
        self.id = -1

    def setID(self, id):
        self.id = id

    def printSelf(self):
        print(f"color = {self.color}, ID = {self.id}")

    def run(self):
        # check if fitting room is empty
        fullStatus = full.acquire(blocking=False)
        mutex.acquire()
        # if fitting room is empty, set decline to False
        if (not fullStatus):
            decline = False()
        else
            full.release

        # mutex.acquire()
        # If not full and currently no Color executing
        if status and (color == "None" or color == self.color) and decline == False:
            # if (color == "None"):
            #     print(f"{self.color} only")
            time.sleep(1)
            print("")
            total -= 1
            printSelf(self)
            mutex.release()
            full.release()




def main():
    #Ask user input
    # inputs = askInput()
    inputs = (2, 3, 4)
    numSlots = int(inputs[0])
    numBlue = int(inputs[1])
    numGreen = int(inputs[2])

    # initialize semaphores
    empty = Semaphore(numSlots)
    full = Semaphore(0)
    mutex = Semaphore()


'''
empty semaphore is a sign that there is still a vacant slot in the fitting room.
full semaphore is a sign that there is still at least one thread in the fitting room.
mutex ensures that only one thread can enter or leave the fitting room at a time.
color is global variable which is the color of the fitting room.
decline is boolean variable if the fitting room is full and processes should leave
until the fitting room is empty. It it False until empty is False, then becomes True
until full is False.

Fitting room is empty
set decline to False
Process wants to start
empty.acquire()
mutex.acquire()
# start process
mutex.release()
full.release()

Once fitting room is full,
set decline to True
Process has completed
empty.acquire()
mutex.acquire()
# print process
mutex.release()
full.release()

Once fitting room is empty, switch colors
switch color
'''
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

    global total = numBlue + numGreen
    # while (total > 0):
        # total -= 1

if __name__ == "__main__":
    main()
