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

Primitives:
-----------
- launch a job (script) remotely or locally
- express dependencies between jobs
- have callbacks
- kill remote or local jobs
- launch instances on amazon?

Questions:
----------
- what is the language type? (functional, declarative, imperative) -> imperative
  and functional (lambdas and closures) ?
- is it OO? -> no?
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
