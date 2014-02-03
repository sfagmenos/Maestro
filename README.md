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

#### Vaggelis 
- Summary: A language to run a script/operation or a function in a poll of workers.
- Pros and cons: It seems to me the most interesting scenario to implement.
- programming languages: Python is ok, but c should be easy too.
- Example:
```
worker *workers = {A, B, C};    
worker D;    
int pool_id;    
pool_id = initialize(workers);        /* initialize a poll of workers */    
broadcast(pool_id, operation1);  /* this should be non-blocking operation/    
pool_id = ammend(pool_id, D);      /* increase pool of workers */    
execute(pool_id, operation2);    /* non-blocking operation */ 
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
course(tlp)
course(os)
course(aos)
professor(aho,[tlp])
professor(yang,[os,aos])
class(2014,[tlp,os],devil_week)
schedule(class)
print devil_week;
```

Ingredients to recipes:
-----------------------
####Arun
-The language will load all the available ingredients
-The kind of recipe that is expected has to be mentioned (breakfast, dessert, etc.)
-There are more details that will need to be discussed. This is just a rough sketch.

Arun wants to decide what to make for breakfast. He gives the program the ingredients currently present in his pantry. 

```
create pantry arunPantry
{
	{	partySize = 1;
		mealType = breakfast;
		mealWeight = light;
	}

	{	item = tomato;
		quantity = 3L;
		class = general;
	}

	{	item = eggs;
		quantity = 1D;
		class = breakfast;
	}

	{	item = onions;
		quantity = 0.5L;
		class = general;
	}

	{	item = whiteRice;
		quantity = 4L;
		class = rice;
	}

}


use pantry arunPantry
void main()
{
	for each ingredient in pantry
		{
			if class == ‘breakfast’ 
				{ include ; }
			else if class == ‘general’
				{include ; }
		}

	generateRecipe();
}
```			

#### Vaggelis 
- Summary: A language to come up with recipies given some ingredients.
- Pros and cons: On the one hand, this one seems the most childish one. 
On the other hand, it  will be the easiest to do, and also Aho gonna like it.
- programming languages: C is perfect for this one.
- Example:
```
vegetable v1 = {onions: 2, tomato: 7, spinach: 1, lettuce: 1, cucumber: 3}    
frout f1 = {orange: 3, mandarin: 10, babana: 5, apple: 5, apricot: 1, grape:2}    
meet  m1 ={pork_chops: 1, beef_steak: 3}    
    
    make_salad(v1, f1, m1)    
    make_lunch(v1, f1, m1)    
    make_lunch(v1, f1, m1, vegetrerian)    
    make_dinner(v1, f1, m1)    
    make_dinner(v1, f1, m1, vegetrerian
```



Name
====
- if you only have a name, it's already a good start


Comments
========
- Let's put our example into a txt file, because the markup format of the README is not appropriate.
