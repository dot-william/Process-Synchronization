from threading import Thread
import time
def run():
    print("Running")
    time.sleep(1)
    print("done")

x = Thread(target=run)
arr = []
arr.append(x)
print(arr[0].ident)
print(arr[0].is_alive())
arr[0].start()
print(arr[0].ident)
print(arr[0].is_alive())
# print(x.ident)
# print(x.is_alive())
# x.start()
# print(x.ident)
# print(x.is_alive())
# time.sleep(3)
# print(x.ident)
# print(x.is_alive())
# x.start()
