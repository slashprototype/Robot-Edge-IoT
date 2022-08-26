
# Importing the modules
import threading
import sys
import time
 
# Custom Exception Class
class MyException(Exception):
    pass

i = 0
try:
    while (i<10):
        print(i)
        if i == 5:
            raise MyException
        i = i + 1

except MyException:
    print(i)
    print('has ended')