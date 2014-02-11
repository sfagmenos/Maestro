Idea
====
A language to express dependencies between jobs and distribute them on many
workers.

Names
-----
- lmdtfy (let me distribute that for you)
- nacl (not another configuration language)

Usecases:
---------
- you want to create and run 2 jobs a and b in parallel, on a few workers. And then
you want to run job c on some workers, only after both a and b succeeded. If some of a or b
fail you want to stop everything and send an email
- you have 3 jobs running with different priorities. job a is the most important but can start
only between 3 and 4 pm. Job b is a bit less important, there is only 1 running, and when it
is done you want to launch a new one. Job c is the least important but you need to launch it
1000 times so it should run on any available machine not taken by a or b
- you want to check that the new release of your program will be compatible with all the architectures

Primitives:
-----------
- launch a job (script) remotely or locally
- express dependencies between jobs
- have callbacks
- kill remote or local jobs
- launch instances on amazon?
- compile the source code

Questions:
----------
- what is the language type? (functional, declarative, imperative) -> imperative
  and functional (lambdas and closures) ?
- is it OO? -> no?
  - this could be yes for adding jobs with certain functionality for some languages (is it C,C++? compile the source first)
- what kind of types do we want? (hidden or explicit, can a user define new
  types)?
- is data mutable? -> I think no, we duplicate to add stuff (because when we run
  a job we can't mutate it it's too late)
- can we preempt jobs?

Remarque:
---------
- interpreted with a REPL would be nice
- We need great error checking, similar to go maybe:
```
if a, err := run_job(my_job), err != nil {
  // handle error
}
// no error
```
- I think we need lambdas, closures would be great

Examples:
=========
#### Mathias
```
// should run all the time, keep going if b fails but die
// if a fails
Batch bg = Job.new('bg.sh', number = 10)

Batch a = Job.new('my_scipt_a.py', number = 10)
Batch b = Job.new('my_scipt_b.rb', number = 5)

func failure_callback(job j) {
  kill_all_jobs
}

func job_killer(Job[] jobs) {
  return func () {
    for j in jobs {
      j.kill_all
    }
  }
}  // here we use a closure

a.on_failure = func(Batch b) {
  kill_all_jobs
}  // with a lambda
b.on_failure = job_killer([a,b]) // with a function pointer/closure

Batch c = Job.new('my_scipt_c.sh', number = 1)
c.add_dependencies([a,b])

run_jobs_async([bg, a, b, c])
```

```
// we want to run a first job and then lauch scemario 2
// if it succeded

Job config = Job.new('config_script', number = :all)
if _, err := run_jobs([config]), err != nil {
  // it failed
  exit -1
}

// it didn't fail, and it was easier than setting it
// as a dependency for all of the jobs
Job a = Job.new('my_scipt_a.py', number = 10, priority = 0)
Job b = Job.new('my_scipt_b.rb', number = 1, priority = 1)
Job c = Job.new('my_scipt_c.sh', number = 1000, priority = 5)

a.can_start = func (Job j) {
  t = Time.now
  pm3 = Time.today(15)
  pm4 = Time.today(16)
  return pm3 <= t  && t <= pm4
}

b.on_success = func (Job j) {
  run_jobs_async([j])  // b finished, relaunch it
}

run_jobs_async([a, b, c])
```

```
// want to make measurement that are in 3 steps: populate, collect
// data and analyse.
// This on is actually pretty complex logic but not that hard to express

func an_hour_after(Job j) {
  return func () {
    j.finish_time && j.finish_time - Time.now > Time.hour(1)
  }
}

Job b = nil
for i in range(0,10) {
  a = Job.new('send_email_batch_'+i+'.rb', number = 1)
  if b { a.add_dependencies([b]) }
  b = Job.new('collect_data.rb', number = 1)
  b.add_func_dependency( an_hour_after(a) )
  Job c = Job.new('anaoyse.py', number = :all)
  c.add_dependecies([b])
  run_jobs_async([a, b, c])
}
```


####Vaggelis
* I see the need to define actions taken when a job starts and completes execution.
*Couldn't we exppress it with handlers?
* callbacks are helpfull; would be nice to support.
* I don't realy see  the need for closures.


```
/* defines how you kill a job */
function callback_killer(Job j){	   
	kill j
}

/* callback for items in second argument */
function kill_all(function killer, Job[] jobs) {
	for j in jobs:
		killer(j)		 
}

/* exit-handler for Jobs */
function kill_all_if_fail(Job[] jobs){  
	if Job.exit_code != NULL:
		kill_all(callback_killer, jobs) 
		exit -1
}


Pool p = Pool.new("128.33.33.1", "128.33.33.2", "128.33.33.3")	/* initialize and update pool of workers*/
p.append("128.33.33.4")				
p.delete("128.33.33.1")					

Job a = Job.new("abc.pl")		      /* scripts corresponding to jobs */ 
Job b = Job.new("xRay.rb")		
Job c = Job.new("telesphorus.py")	

a.exit_handler(kill_all_if_fail)	/* handler executed when Job terminates */
b.exit_handler(kill_all_if_fail)	
c.dependency([a,b])			          /* indicate that c runs after a, b successful execution */

p.run([a, b, c]) /*run is ok; run_async is wrong because we have dependency, thus it isn't async */

```




```

function is_time(Job j){	 
	return Time.now.hour > 15 && Time.now.hour < 16
}

function relaunch_on_sucess(){
	if Job.exit_code == NULL
		p.run(Job)
}

function run_1000(Job j){
	counter = 0
	return function run(){
		if ++counter < 1000:
			return p.run(j)
	}
	

Pool p = Pool.new("128.3.3.1", "128.3.3.2")	/* initialize pool of workers*/

Job a = Job.new("abc.pl", priority=0)		    /* zero is lowest priority */
Job b = Job.new("xRay.rb", priority=1)		
Job c = Job.new("telesphorus.py", priority=2)	

a.start_handler(is_time)		                /* job starts executing when start_handler returns 1 */
b.exit_handler(relaunch_on_success)	        /* exit_handler is executed when job terminate */
c.exit_handler(run_1000)

p.run([a, b, c]) 

```

### Ren

// input a list of programs in order, using right arrows to indicate dependencies and and bidirectional arrows to indicate programs to run in parallel.
// should have something that allows us to specify "on available machines" - and use that to show priorities
// my intuition is to handle with more logic

Scenario 1
```
def raiseError():
	 killjobs(job)
	 sendEmail()


 Try: 
      Job job = Job.new([('program_a.py'<-->'program_b.py')--> 'program_c.py'])
 Except:
	raiseError(job)
```	

Scenario 2:
```
def currentTime():
	 return Time.now.hour


Try:
	While True:
	      ct = currentTime
	      If 15 < ct < 16:
	      	 Job job_1 = Job.new('program_a.py')
	      
		While availableMachines > 0:
	      	   Job job_2 = Job.new('program_b.py', number=availableMachines)
		
		For i=1:1000:
		    Job job_3 = Job.new('program_c.py', number=availableMachines)
Except:
	raiseError(job_1, job_2, job_3)
```

#### Arun

- Ren's idea seems intuitive. 
- I had thought of single arrow (-->) and double arrow (-->>)
- But using uni-directional and bi-directional arrows would make it easily understandable. 
- I don't see the requirements for closures. They might make it complicated.
- Maybe include the priority along with the program?

```

Scenario 1. Equal priorities.

def raiseError():
	 killjobs(job)
	 sendEmail()


 Try: 
      Job job = Job.new([('program_a.py', priority = 0 <--> 'program_b.py', priority = 0)--> 'program_c.py', priority = 0])
 Catch:
	raiseError(job)
	
```

Scenario 2

```
def currHour():					/* return current hour of the day in float*/
	return current_hour_of_the_day
	
def scanMachines():				/*return number of machines not executing any job*/
	return no_of_idle_machines
		
def status(job):				/*return the status of a job*/
	return 0 if job is not running
	return 1 if job is running
	
count = 0
	
Workers w = Workers.new ("xxx.xxx.xxx.xx", "xxx.xxx.xxx.xx", "xxx.xxx.xxx.xx", .....)    /*declare all worker machines*/

try:

	time_now = currHour()

	Loop:
		if time_now between 15 and 16:
			Job job1 = job.new ("1.py", priority = 3)
		
		if status("2.py") == 0
			Job job2 = job.new ("2.py")
	
		while count < 1000:
			Job job3 = job.new ("3.py", number = scan_Machines()) /*number defines number of machines to execute the job on*/
			c++
	
catch:
	raiseError(job1, job2, job3)
```

### Georgios

// Create the jobs you want to run.
// Check if all are syntactically correct/compiling (this could be done in initialization)
// Create dependencies (Ren's idea with arrows is nice)
// Run jobs in the datacenter/cloud

```
def run(time,architecure,datacentre):

Job a = Job.new("my_program","C")
Job b = Job.new("new_feauture","C")
if a.compiles() and b.compiles():
	Job c = a.link(b)
	c.run("15:00","x86_64","amazon")

Job c = Job.new("new_feature2.py","Python")
Job d = Job.new("program_d.py","Python")
Job e = Job.new("program_e.py","Python")
if not c.sompile() or not d.sompile() or not e.sompile():
	exit("Compilation errors")
Batch all = Batch.new([(d<->e)->c])
```
