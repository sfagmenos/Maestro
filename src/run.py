import sys
from maestro_cmd import Console
from myacc import *
import threading
from helpers import jobqueue

if __name__ == '__main__':
    threading.Thread(target=jobqueue.GlobalJobQueue.poll_for_jobs).start()
    if len(sys.argv) == 1:
        console = Console(parser)  # while True:
        console.cmdloop()  # try:
    elif len(sys.argv) == 2:
        try:
            f = open(sys.argv[1])
        except IOError:
            print 'cannot open', sys.argv[1]
            sys.exit(-1)
        prgm = f.read()
        result = pipeline(prgm)
        print result
        f.close()
    else:
        print "Usage: python myacc.py <file_name>"
    jobqueue.GlobalJobQueue.stop()
