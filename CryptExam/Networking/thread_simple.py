import threading 

def someFunc(numb):
    print 'someFunc was called' + str(numb)

t1 = threading.Thread(target=someFunc, args=(1,))
t1.start()

t1.join()
 
