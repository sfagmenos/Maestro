'''
Implementation of semantic actions
'''
from networkx import DiGraph
import pickle
import redis
import jobqueue
import subprocess
import time
import uuid
import os


depen_graph = DiGraph()

class Job():
    '''Constructor of class should be supplied with job name and
    respective script name
    '''
    def __init__(self, script='', arguments=[]):
        self._dependencies = []
#        self._workers = workers
        self._script = script
        self._arguments = arguments
        self._stderr = None
        self._stdout = None
        self._errno = None  # errno is None since job has not run
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
        #jobqueue.GlobalJobQueue.enqueue(self)

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

    def run_localy(self):
        '''run a job localy'''
        # need error checkong of what Popen returns
        try:
            args = [self._script]
            args += self._arguments
            s = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            self._stdout, self._stderr = s.communicate()
            self._errno = s.returncode
            self._log()
        except Exception, error:
            print "Unhandled Exception:", error, "for job:", self._script,\
                    "with arguments:", self._arguments
            return

    def run_remotely(self, host, port, channel):
        '''run a job remotelly'''
        try:
            connection_pool = redis.Redis(host, port)
        except Exception, error:
            print "Redis Error:", error
            return

        # read script and publish it to channel
        try:
            f = open(self._script, "r")
            arguments = self._arguments
            script_body = f.read()
            f.close()
        except Exception, error:
            print "Unable to open script:", self._script
            print "Exception:", error
            return

        # construct message. First line is the arguments,
        # following lines are the body of the script
        msg = {'job_key': uuid.uuid1().hex,\
                     'job_arguments': ' '.join(arguments),\
                     'script_body': script_body}
        # encode
        pickled = pickle.dumps(msg)

        # publish message
        connection_pool.publish(channel, pickled)

        # get response
        self._stdout, self._stderr = None, None # should be returned by redis
        self._errno = 0 #should be returned by redis
        self._log()
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


def add_dependencies(jobs, depend_on):
    for job in jobs:
        job.add_dependency(depend_on)


def run(JobsList):
    '''Enqueue jobs'''
    if isCyclic(depen_graph):
        print "Your jobs have circular dependencies"
        return False

    # print some stats so that user knows what's going on
    for job in JobsList:
        print "Job: \"%s\"" % job.script(),\
                    "has: %d" % len(job.dependencies()),\
                    "unresolved dependencies."
        jobqueue.GlobalJobQueue.enqueue(job)


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
