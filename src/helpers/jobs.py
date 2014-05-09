'''
Implementation of semantic actions
'''
from networkx import DiGraph
import subprocess
import time
import os


def isCyclicUtil(graph, vertex, visited, recstack):

    if not visited[vertex]:
        visited[vertex] = True
        recstack[vertex] = True
    for des in graph.successors(vertex):
        if not visited[des] and isCyclicUtil(graph, des, visited, recstack):
            return True
        elif recstack[des]:
            return True
    recstack[vertex] = False
    return False


def isCyclic(graph):

    visited = {}
    recstack = {}
    for node in graph.nodes():
        visited[node] = False
        recstack[node] = False
    for node in graph.nodes():
        if isCyclicUtil(graph, node, visited, recstack):
            return True
    return False


depen_graph = DiGraph()


class Job():
    '''Constructor of class should be supplied with job name and
    respective script name
    '''
    def __init__(self, script='', arguments=[], deps_jobs=None, deps_args=None):
        self._dependencies = []
#        self._workers = workers
        self._script = script
        self._arguments = arguments
        self._stderr = None
        self._stdout = None
        self._errno = None  # errno is None since job has not run
        self._deps_jobs = deps_jobs
        self._deps_args = deps_args
        depen_graph.add_node(self)
        # log is not needed if any script is associated
        if not script:
            return
        # create log file; truncate it if it exists
        self._logfile_name = os.getcwd() + '/' + self._script + ".log"
        try:
            self.f = open(self._logfile_name, "w")
        except Exception, error:
            print "Unhandled Exxception:", error,\
                    " while creating log file for job:", self._script
        self.f.close()

    def stdout(self):
        return self._stdout

    def script(self):
        return self._script

    def dependencies(self):
        return self._dependencies

    def perror(self):
        return self._errno, self._stderr

    def add_dependency(self, depends_on):
        '''Add names of jobs on which current object
        depends on.
        '''
        for job in depends_on:
            self._dependencies.append(job)
            depen_graph.add_edge(self, job)

    def compute_args(self):
        if self._deps_args:
            self._arguments = self._deps_args(sum([j.stdout().split("\n") \
                            for j in self._deps_jobs], []))

    def run(self):
        '''this should do the remote execution of scripts'''
        # need error checkong of what Popen returns
        try:
            self.compute_args()
            args = [self._script]
            args += self._arguments
            # print args
            s = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            self._stdout, self._stderr = s.communicate()
            self._errno = s.returncode
            self._log()
        except Exception, error:
            print "Unhandled Exception:", error, "for job:", self._script,\
                    "with arguments:", self._arguments
            return

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

    def _log(self):
        # file is created by class constructor. Append logs.
        f = open(self._logfile_name, "a")
        print >> f, "STDOUT:"
        print >> f, "---------"
        print >> f, self._stdout
        print >> f, "---------"
        print >> f, "STDERR:"
        print >> f, "---------"
        print >> f, self._stderr
        print >> f, "#########"
        f.close()


class Wait(Job):
    '''fake class to create wait objects'''
    def __init__(self, sleepinterval):
        Job.__init__(self)
        self._sleepinterval = int(sleepinterval)

    def run(self):
        time.sleep(self._sleepinterval)
        self._errno = 0

    def _log(self):
        pass


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
    if isCyclic(depen_graph):
        print "Your jobs have circular dependencies"
        return False
    # print some stats so that user knows what's going on
    print "Job-queue:", [job.script() for job in Queue]
    print "----------"
    for job in Queue:
        print "Job: \"%s\"" % job.script(),\
                "has: %d" % len(job.dependencies()),\
                "unresolved dependencies."
    print "----------"
    while Queue:
        for job in Queue:
            if job.can_run():
                print "Running job: \"%s\"" % job.script()
                Queue.remove(job)
                job.run()
                (errno, stderr) = job.perror()
                if errno != 0:
                    print "Error while executing Job: \"%s\"" % job.script()
                    print stderr
        time.sleep(0.5)
