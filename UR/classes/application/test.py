import time
from threading import Thread



def loop():
    while True:
        try:
            time.sleep(1)
            print(1)
        except KeyboardInterrupt:
            th.join(timeout=1)
            break

th = Thread(target=loop)
th.start()

while True:
    try:
        time.sleep(0.5)
        print('main')
    except KeyboardInterrupt:
        th.join(timeout=1)