from lib.Class import *
from lib.Events import *
from lib.Environment import *
import threading

try: 
    import queue
except ImportError:
    import  Queue

# Gen and Init thread 
def main():

    luffy = Luffy() # init player
    queue = Queue.Queue(10) # init queue
    #Env = Environment()
    """
    Creates 2 Threads of command to queue keyboard and mouse actions
    and calls Run() from class Luffy to start main player looping
    """
    #thread_Command = threading.Thread(target=(Commands), args=(queue,))
    thread_Luffy = threading.Thread(target=(luffy.Run), args=(queue,))
    #Env.Run()
    try:
        #thread_Command.start()
        thread_Luffy.start()
    except:
        print "Failed to load Thread(s)"

if __name__ == "__main__": main()
