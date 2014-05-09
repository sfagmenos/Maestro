'''
Implementation of job queue
'''
import jobs
import time
import threading

class JobQueue():
    def __init__(self):
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

    def execute(self, job):
        if job.can_run():
            print "Running job: \"%s\"" % job.script()
            job.run()
            (errno, stderr) = job.perror()
            if errno != 0:
                print "Error while executing Job: \"%s\"" % job.script()
                print stderr
            else:
                print job.stdout()
            self.dequeue(job)

    def poll_for_jobs(self):
        '''Thread main loop'''
        while self._Run or self._Q:
            # loop on a copy of the queue to avoid deadlocks 
            temp = list(self._Q)
            for job in temp:
                if job.can_run():
                    threading.Thread(target=self.execute, args=[job]).start()
            time.sleep(0.5)

    def sort(self):
        sorted(self._Q, key=lambda x: x.soft_priority)



GlobalJobQueue = JobQueue() # construct global queue
GlobalServiceHost = ''
GlobalServicePort = ''
