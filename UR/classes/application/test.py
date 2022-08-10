import time
from threading import Thread
import sys

interrup = False

def loop():
    while True:
        time.sleep(1)
        print(1)
        if interrup == True:
            break

th = Thread(target=loop)
th.start()

while True:
    try:
        time.sleep(0.5)
        print('main')

    except KeyboardInterrupt:
        interrup = True
        th.join()