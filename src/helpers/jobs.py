'''
Implementation of semantic actions
'''

import subprocess
import time


class Job():
    '''Constructor of class should be supplied with job name and
    respective script name
    '''
    def __init__(self, name, script, workers=1):
        self._dependencies = []
        self._workers = workers
        self._script = script
        self._stderr = None
        self._stdout = None
        self._errno = None  # errno is None since job has not run
        self._name = name

    def stdout(self):
        return self._stdout

    def perror(self):
        return self._errno, self._stderr

    def __repr__(self):
        return self._name

    def add_dependency(self, depends_on):
        '''Add names of jobs on which current object
        depends on.
        '''
        for job in depends_on:
            self._dependencies.append(job)

    def run(self):
        '''this should do the remote execution of scripts'''
        # need error checkong of what Popen returns
        ip = 'localhost'
        try:
            #s = subprocess.Popen(self._script, stdout=subprocess.PIPE)
            s = subprocess.Popen(['rsh',ip,self._script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError, error:
            self._stdout = None
            self._stderr = error
            self._errno = -1
            return

        streamdata = s.communicate()
        self._stdout = streamdata[0]
        self._stderr = streamdata[1]
        self._errno = s.returncode

    def can_run(self):
        '''check if dependencies are fullfilled.
        Current instrance can run only if all jobs from
        its dependency list have successed ( errno is zero )
        '''
        if not self._dependencies:
            return True
        for job in self._dependencies:
            if job.perror()[0] != 0:
                return False
        return True


class JobQueue:
    '''Construct job queue as a list whose first element
    are job names of jobs with zero dependencies,
    second are job names of jobs with one dependency, etc.
    '''
    def __init__(self,  MaxDependencies=10):
        self.Q = []
        for _ in range(MaxDependencies):
            self.Q.append([])

    def enqueue(self, job, dependencies):
        self.Q[dependencies] = job


def add_dependencies(jobs, depend_on):
    for job in jobs:
        job.add_dependency(depend_on)


def run(Queue):
    '''Try to run job from queue'''
    # suppose queue is constructed.
    #
    # e.g. Q = [[a,b],[c]], means that jobs with one
    # dependency i.e., Q[0] = [a,b] should run before
    # jobs with two dependencies, i.e., Q[1] = [c]
    #
    while not Queue[i]:
        for job in Queue[i]:
            if job.can_run():
                Queue[i].remove(job)
                job.run()
        time.sleep(0.5)
