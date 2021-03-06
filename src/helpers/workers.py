'''
Workers API
'''
import urllib
import jobqueue
import json
import redis
import subprocess
import  os
import signal
import sys
import uuid

def signal_handler(signal, frame):
    print "\nSee u soon :-)\nGoodBye!"
    sys.exit(0)

signal.signal(signal.SIGQUIT, signal_handler)

class worker():
    '''Constructor of class'''
    def __init__(self, host_port='', channel=''):
        jobqueue.GlobalJobQueue.stop()
        self.worker_key = job_key = uuid.uuid1().hex
        # get arguments
        try:
            self.host = host_port.split(':')[0]
            self.port = host_port.split(':')[1]
            if not channel:
                self.channel = 'maestro_channel'
            else:
                self.channel = channel
        except Exception, error:
            print "Malformed IP:PORT pair:\"%s\"" % ip_port
            print error
            return

        # instanciate pool
        try:
            self.connection_pool = redis.Redis(self.host, self.port)
            print "Connection pool at: <%s:%s>" % (self.host, self.port)
        except Exception, error:
            print "Failed to launch ConnectionPool"
            print error
            return
         
        #subscribe to channel
        try:
            self.pubsub = self.connection_pool.pubsub()
            self.pubsub.subscribe(self.channel)
        except Exception,  error:
            print "Unable to subscribe to channel"
            print error
            return

        # start polling for messages
        print "Polling for messages"
        for item in self.pubsub.listen(): 
            if item['type'] == 'message':
                # if exception keep up the server. The client may
                # get a bad response, but the server must survive
                try:
                    self.execute(item)
                except Exception, error:
                    print  "Unhandled Exception:", error
                    continue

    def execute(self, item):
        '''function to run job localy and publish back its output'''
       # decode request body
        request = json.loads(item['data'])

        jobs_worker = request['jobs_worker']

        # if job is not assigned to you terminate
        if jobs_worker != getexternalip():
            return

        #parse request
        job_key = request['job_key']
        arguments = request['job_arguments'].split(' ')[:]
        script_body = request['script_body']
        script_name = request['script_name']

        # create temp file
        f = open("./this_will_never_exist.sh", "w")
        f.write(script_body)
        f.close()
        try:
            os.chmod("./this_will_never_exist.sh", 0766)
        except Exception, error:
            print "Unhandled Exception:", error

        # execute command
        pcommand = ['./this_will_never_exist.sh'] + arguments
        s = subprocess.Popen(pcommand, stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
        # print what you executed

        print "Just executed job:", script_name,\
                 "with arguments:", arguments

        # get return values
        stdout, stderr = s.communicate()
        errno = s.returncode

        # remove temp file
        os.remove("./this_will_never_exist.sh")

        # send back response to custom job channel
        response = {'stdout': stdout,
                     'stderr': stderr,
                     'errno': errno}
        
        jresponse = json.dumps(response)
        self.connection_pool.publish(job_key, jresponse)


def getexternalip():
    '''This function returns the external IP of the machine.
    Subscribers are registered in Redis channel with their
    external IP, which is used to identify them when jobs
    are dispatched
    '''
    ip = urllib.urlopen('http://www.biranchi.com/ip.php').read()
    return ip[3:]
