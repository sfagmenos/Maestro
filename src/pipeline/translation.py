import helpers.jobs as hj

def execute(ast, sym_table):
    op = ast.operation
    if ast.leaf:  # we have a leaf, just return the value associated
        if op == 'id':
            return sym_table[ast.value][0]
        else:
            return ast.value

    if op == 'prgm':
        ast.value = execute(ast.children[0], sym_table)
        return ast.value
    elif op == 'stmt-list':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = children_exec[-1]
        return ast.value
    elif op == 'Job':  # all args should be strings
        children_exec = [execute(c, sym_table) for c in ast.children][0]
        args = children_exec
        ast.value = hj.Job(args[0], args[1:])
        return ast.value
    elif op == 'Wait':  # 1 int arg
        ast.value = hj.Wait(ast.children[0])
        return ast.value
    elif op == 'run':
        children_exec = [execute(c, sym_table) for c in ast.children][0]
        ast.value = hj.run(flatten(children_exec))
        return ast.value
    elif op == 'range':
        arg = execute(ast.children[0], sym_table)
        ast.value = range(arg[0])
        return ast.value
    # elif op == 'map':
        # list_of_job_arguments = [execute(c, sym_table) for c in ast.children[0]]
        # name_of_map_script = execute(ast.children[1])
        # for x in list_of_job_arguments:
            # sym_table[] = [x, ]
            # hj.run(name_of_map_script)
        # children_exec = [execute(c,sym_table) for c in list_of_jobs]
        # dep(children_exec[0], children_exec[1])
        # ast.value = 
        # return ast.value
    # elif op == 'reduce':
        # maps = ast.children[0]
        # reduce_script = ast.children[1]
        # ast.value =
        # return ast.value
    elif op == 'list-loop':
        var = ast.children[1].value
        l = execute(ast.children[0], sym_table)
        for x in l:
            sym_table[var] = [x, '???']
            execute(ast.children[2], sym_table)
    elif op == '=':
        children_exec = execute(ast.children[-1], sym_table)
        sym_table[ast.children[0]] = [children_exec, ast.children[-1]._type]
        ast.value = children_exec
        return ast.value
    elif op == 'list':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = children_exec[0]
        return ast.value
    elif op == 'list-concat':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = children_exec[0] + [children_exec[-1]]
        return ast.value
    elif op == 'list-orig':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = children_exec
        return ast.value
    elif op == '<->':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = nodep(children_exec[0], children_exec[1])
        return ast.value
    elif op == '->':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = dep(children_exec[0], children_exec[1])
        return ast.value
    elif op == '+':
        children_exec = [execute(c, sym_table) for c in ast.children]
        t1 = ast.children[0]._type
        t2 = ast.children[1]._type
        if t1 == 'string' and t2 == 'int':
            ast.value = children_exec[0] + str(children_exec[1])
        elif t2 == 'string' and t1 == 'int':
            ast.value = str(children_exec[0]) + children_exec[1]
        else:
            ast.value = reduce(lambda x,y: x+y, children_exec)
        return ast.value
    elif op == '-':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = children_exec[0] - children_exec[1]
        return ast.value
    elif op == '/':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = children_exec[0] / children_exec[1]
        return ast.value
    elif op == '%':
        children_exec = [execute(c, sym_table) for c in ast.children]
        ast.value = children_exec[0] % children_exec[1]
        return ast.value
    else:
        return None

# flatten helper: flattens a list of embeded lists
def flatten(lst):
    return sum( ([x] if not isinstance(x, list) else flatten(x)
             for x in lst), [] )

# Dependencies helper
def nodep(ljobs, rjobs):
    if type(ljobs) is not list:
        ljobs = [ljobs]
    if type(rjobs) is not list:
        rjobs = [rjobs]
    return flatten(ljobs + rjobs)

def dep(jobs, depend_on_jobs):
    if type(jobs) is not list:
        jobs = [jobs]
    if type(depend_on_jobs) is not list:
        depend_on_jobs = [depend_on_jobs]
    hj.add_dependencies(jobs, depend_on_jobs)
    return flatten(jobs + depend_on_jobs)
