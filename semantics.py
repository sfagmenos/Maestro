'''
Implementation of semantic actions
'''

from subprocess import Popen, wait


# This is a dictionary keeping all
# Jobs that have been constructed.
Jobs = dict()


class Job():
    '''Constructor of class should be supplied with job name and
    respective script name
    '''
    def __init__(self, name, script, dependencies=None, workers=1):
        self.dependencies = dependencies
        self.workers = workers
        self.script = script
        self.stderr = None
        self.stdout = None
        self.errno = None  # errno is None since job has not run
        Jobs[name] = self
        self.name = name

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
        '''check if dependencies are fullfilled.
        Current instrance can run only if all jobs from
        its dependency list have successed ( errno is zero )
        '''
        for job in self.dependencies:
            if Jobs[job].perror() != (0, _):
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


def run(Queue):
    '''Try to run job from queue'''
    # suppose queue is constructed.
    #
    # e.g. Q = [[a,b],[c]], means that jobs with one
    # dependency i.e., Q[0] = [a,b] should run before
    # jobs with two dependencies, i.e., Q[1] = [c]
    #
    for i in range(len(Queue)):
        while not Queue[i]:
            for job in Queue[i]:
                if job.can_run():
                    Queue[i].remove(job)
                    job.run()
