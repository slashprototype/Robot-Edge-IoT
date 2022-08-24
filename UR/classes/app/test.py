
# Importing the modules
import threading
import sys
 
# Custom Exception Class
class MyException(Exception):
    pass
 
# Custom Thread Class
class MyThread(threading.Thread):
     
  # Function that raises the custom exception
    def someFunction(self):
        name = threading.current_thread().name
        raise MyException("An error in thread "+ name)
 
    def run(self):
       
        # Variable that stores the exception, if raised by someFunction
        self.exc = None           
        try:
            self.someFunction()
        except BaseException as e:
            self.exc = e
       
    def join(self):
        threading.Thread.join(self)
        # Since join() returns in caller thread
        # we re-raise the caught exception
        # if any was caught
        if self.exc:
            raise self.exc
 
# Driver function
def main():
    while True:
        # Create a new Thread t
        # Here Main is the caller thread
        t = MyThread()
        t.start()
        
        # Exception handled in Caller thread
        try:
            t.join()
        except Exception as e:
            print("Exception Handled in Main, Details of the Exception:", e)
    
# Driver code
if __name__ == '__main__':
    main()


x = False
y = False
z = True

if (x or y or z) != False:
    print('hay alarma')
else:
    print('no hay alarma')