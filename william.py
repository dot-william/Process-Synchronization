import threading
from threading import Thread, Semaphore
import time
import random

fittingRoom = None
id = 1
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
        t = threading.Thread(target=executeThread, args=(color, id))
        id+=1
        t.start()
        queue.append(t)

def executeThread(color, id):
    global fittingRoom
    fittingRoom.acquire()
    print(f"Thread ID = {id}, color = {color}")
    time.sleep(2)
    fittingRoom.release()

def main():
    global fittingRoom
    #Ask user input
    # inputs = askInput()
    inputs = (2, 3, 4)
    numSlots = int(inputs[0])
    numBlue = int(inputs[1])
    numGreen = int(inputs[2])
    threads = []
    fittingRoom = Semaphore(numSlots)

    createThreads(threads, numBlue, 'Blue')
    createThreads(threads, numGreen, 'Green')
    # for thread in threads:
    #     thread.join()


if __name__ == "__main__":
    main()



