import threading
from threading import Thread, Semaphore
import time
import random

# global empty, full, and mutex semaphores
empty = Semaphore()
full = Semaphore()
mutex = Semaphore()

def askInput():
    numSlots = input("Enter the number of slots inside the fitting room: ")
    numBlueThreads = input("Enter the number of blue threads: ")
    numGreenThreads = input("Enter the number of green threads: ")
    return numSlots, numBlueThreads, numGreenThreads

def createThreads(queue, numThreads, color):
    for _ in range(numThreads):
        t = ColoredThread(target=run, color=color)
        queue.append(t)

def signal():
    pass

def printQueue(queue):
    for t in queue:
        t.printSelf()
    print()

class ColoredThread(Thread):
    global empty, full, mutex
    def run():
        time.sleep(1)
        print("")
        print("done")

    def __init__(self, target, color):
        Thread.__init__(self, target=run)
        self.color = color
        self.id = -1

    def setID(self, id):
        self.id = id

    def printSelf(self):
        print(f"color = {self.color}, ID = {self.id}")

def main():
    #Ask user input
    # inputs = askInput()
    inputs = (2, 3, 4)
    numSlots = int(inputs[0])
    numBlue = int(inputs[1])
    numGreen = int(inputs[2])

    # create semaphores
    empty = Semaphore(numSlots)
    full = Semaphore(0)
    mutex = Semaphore()

    # Create thread
    queue = []
    createThreads(queue, numBlue, 'b')
    createThreads(queue, numGreen, 'g')

    printQueue(queue)

    # Shuffle the elements
    random.shuffle(queue)

    printQueue(queue)

    # assign thread IDs
    id=1
    for t in queue:
        t.setID(id)
        id += 1

    printQueue(queue)

    # Pop the threads, if statement so taht there wont be a mix of blue and green, to the waiting Queue

    # Can't execute

    # Threads not able to get into fitting room waits for an available room to open

    # when room is empty, process gets into the room

    # There is n number of threads waiting

    # So there will be a certain



    # 1 room == 1 binary semaphore
    # all initialized to 1



if __name__ == "__main__":
    main()
