import threading
import time
import random


def run():
    time.sleep(1)
    print("")
    print("done")

def askInput():
    numSlots = input("Enter the number of slots inside the fitting room: ")
    numBlueThreads = input("Enter the number of blue threads: ")
    numGreenThreads = input("Enter the number of green threads: ")
    return numSlots, numBlueThreads, numGreenThreads

def createThread(queue, numThreads):
    for _ in range(numThreads):
        t = threading.Thread()
        queue.append(t)

def signal():
    pass

def main():
    #Ask user input
    inputs = askInput()
    numSlots = input(0)
    numBlue = input(1)
    numGreen = input(2)

    # Create thread
    queue = []
    createThread(queue, numBlue)
    createThread(queue, numGreen)

    # Shuffle the elements
    random.shuffle(queue)

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
