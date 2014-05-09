'''
Implementation of job queue
'''
import jobs
import time
import threading

class JobQueue(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.mutex = threading.Lock()
        self._Q = []
        self._Run = True

    def enqueue(self, job):
         self.mutex.acquire()
         self._Q.append(job)
         self.mutex.release()

    def dequeue(self, job):
        self.mutex.acquire()
        self._Q.remove(job)
        self.mutex.release()
    
    def stop(self):
        self._Run = False
    
    def run(self):
        '''Thread main loop'''
        while self._Run or self._Q:
            temp = list(self._Q)
            for job in temp:
                if job.can_run():
                    print "Running job: \"%s\"" % job.script()
                    job.run_remotely('localhost', '6379', 'maestro_channel')
                    (errno, stderr) = job.perror()
                    if errno != 0:
                        print "Error while executing Job: \"%s\"" % job.script()
                        print stderr
                    self.dequeue(job)
            time.sleep(0.5)


GlobalJobQueue = JobQueue() # construct global  queue
