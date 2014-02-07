plt
===

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
- you want to create and run 2 jobs a and b in parrallel, on a few workers. And then
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
  with functional stuff (lambdas and closures) ?
- is it OO? -> no?
- waht kind of types do we want? (hidden of explicit, can a user define new
  types)?
- is data mutable?

Remarques:
----------
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
```
