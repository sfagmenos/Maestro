plt
===

Ideas
=====

Probabilistic:
--------------
#### Mathias
- Summary: a language for stress testing systems with relevant data. The
  language allows you to define distributions, work with them (eg combine
  distributions, generate points from the distribution) and generate complex
  data that follow a pattern.
- Pros and cons: I think the distribution part is fairly straighforward and that
  the application is cool. The distribution manipulation is probably too basic,
  but the adaptation to testing can be challenging. We just need to make sure
  it's not too hard.
- programming languages: C or Python (testing stuff could be made in python)
- Example:
```
generator User {
  field :name
}
generator Action {
  field :type
  distributions type: Normal(1,1)
}

user_generator = User.new
user_generator.creation(Poisson.new(2))
user_generator.max(100)

stress = Action.new
stress.dependency(user_generator, Normal.new(1, 10) + Nomral.new(20, 5))

1000.times do
  stress.generate
end
```

#### Yiren
- A probabilistic programming language to easily specify and perform operations on graphical models 
  - http://mlg.eng.cam.ac.uk/duvenaud/talks/probabilistic-programming-introduction.pdf
  - existing probabilistic languages:
    - stan
    - infer.net
    - church

Distributed Job assignment:
---------------------------
A language for scheduling jobs in a data center (distribute a list of jobs in a datacenter).
#### Mathias
- Summary: a language to script what you want to get done. Some workers kisten
  and when you run the script work is distributed among them with the
  dependencies that are in the script
- Pros and cons: There already better solutions out there but it could be fun to
  implement
- programming languages: we would do a lot of stuff over http so python may be
  better
- Example:
```
init = execute('~/setup.rb')
execute('task1.bash', workers = 10, depends_on = [init])
loop do
  a = execute('populate_data.rb', workers = 5, purge = false)
  b = sleep(100)
  execute_on_workers('crunch_data.bash', a.workers)
end
when_available('low_priority.py')
```

Class Scheduling:
-----------------
- The language will load the courses, teachers, and classes for the school
- Then for each class will have to fill their days with the courses
- There should be a standard of haw many hours the kids can be in classes
  and how many days the week has for teaching. This could be in an init 
  function or loaded by the user.
```
generator course{
  field :name
}
generator professor{
  field :name
  teaches :courses --a list of courses
}
generator class{
  field :year
  teached :courses --a list of courses to be teached
  week :array --an array with the five days with the courses of the class
}
generator day{
  field :array --an array with each cell will be a tuple with th course and the professor
}

```

Ingredients to recipes:
-----------------------


Name
====
- if you only have a name, it's already a good start


Comments
========
- Let's put our example into a txt file, because the markup format of the README is not appropriate.
