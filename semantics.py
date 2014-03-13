'''
Implementation of semantic actions
'''

from Queue import PriorityQueue
from subprocess import Popen, wait


Queue =  dict()
Jobs = dict()

class Job():
    '''Constructor of class should be supplied with job name and
    respective script name
    '''
    def __init__(self, name, script, dependencies=None, workers=1):
        self.script = script
        self.dependencies = dependencies
        self.errno = 0
        self.stderr = None
        self.stdout = None
        self.workers = workers
        self.name =  name
        Jobs[name] = self

    def perror(self):
        return self.errno, self.stderr

    def __repr__(self):
        return self.name

    def add_dependency(self, depends_on):
        '''Add names of jobs on which current object
        depends on.
        '''
        for name in depends_on:
            self.dependencies.append(name) 
    
    def run(self):
        '''this should do the remote execution of scripts'''
       s = subprocess.Popen(self.script, stdout=subprocess.PIPE)
       streamdata = s.communicate()
       self.output = streamdata[0]
       self.stderr = streamdata[1]
       self.errno = s.returncode

    def can_run():
        '''check if dependencies are fullfilled'''
        for job in self.dependencies:
            if Jobs[job].perror() != 0, _ :
                return False
        return True


def run():
    '''construct priority queue'''
    #
    # suppose priority queue is constructed...
    #
    # e.g. Q = [[a,b],[c]], means that jobs with one 
    # dependency i.e., Q[0] = [a,b] should run before 
    # jobs with two dependencies, i.e., Q[1] = [c]   
    #
    for i in range(len(Queue)):
        while not Queue[i]
            for job in Queue[i]:
                if job.can_run():
                    Queue[i].remove(job)
                    job.run()
