from multiprocessing import Process

def f(name):
    while True:
        print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()