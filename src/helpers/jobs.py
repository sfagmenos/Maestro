'''
Implementation of semantic actions
'''
from networkx import DiGraph
import json 
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
    def __init__(self, script='', arguments=[], deps_jobs=None, deps_args=None):
        self._dependencies = []
        self._host = ''
        self._port = ''
        self._channel = ''
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
    
    def set_cluster(self, host, port, channel):
        self._host = host
        self._port = port
        self._channel = channel

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
        self.compute_args
        if not self._host:
            self._run_localy()
        else:
            self._run_remotely()

    def _run_localy(self):
        '''run a job localy'''
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

    def _run_remotely(self):
        '''run a job remotelly'''
        host = self._host
        port = self._port
        channel = self._channel
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
        job_key = uuid.uuid1().hex
        request = {'job_key': job_key,\
                     'job_arguments': ' '.join(arguments),\
                     'script_body': script_body}
        # encode
        jrequest = json.dumps(request)
        # publish message
        connection_pool.publish(channel, jrequest)
        
        # get response in job specific channel
        pubsub = connection_pool.pubsub()
        pubsub.subscribe(job_key)
        for item in pubsub.listen():
            if item['type'] == 'message':
                response = json.loads(item['data'])
                self._stdout = response['stdout']
                self._stderr = response['stderr']
                self._errno = response['errno']
                break

        # log stderr, stdout, and errno
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


def run(JobsList, host='localhost', port='6379', channel='maestro_channel'):
    '''Enqueue jobs'''
    if isCyclic(depen_graph):
        print "Your jobs have circular dependencies"
        return False

    # print some stats so that user knows what's going on
    for job in JobsList:
        job.set_cluster(host, port, channel)
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
