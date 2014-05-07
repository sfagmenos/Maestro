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
        children_exec = [execute(c, sym_table) for c in ast.children]
        args = children_exec
        ast.value = hj.Job(args[0], args[1:])
        return ast.value
    elif op == 'Wait':  # 1 int arg
        ast.value = hj.Wait(ast.children[0])
        return ast.value
    elif op == 'run':
        children_exec = [execute(c, sym_table) for c in ast.children][0]
        ast.value = hj.run(children_exec)
        return ast.value
    elif op == 'range':
        arg = ast.children[0]
        ast.value = range(arg)
        return ast.value
    elif op == '=':
        children_exec = execute(ast.children[-1], sym_table)
        sym_table[ast.children[0]] = [children_exec, ast.children[-1]._type]
        ast.value = children_exec
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
    else:
        return None

# Dependencies helper
def nodep(ljobs, rjobs):
    if type(ljobs) is not list:
        ljobs = [ljobs]
    if type(rjobs) is not list:
        rjobs = [rjobs]
    return ljobs + rjobs

def dep(jobs, depend_on_jobs):
    if type(jobs) is not list:
        jobs = [jobs]
    if type(depend_on_jobs) is not list:
        depend_on_jobs = [depend_on_jobs]
    hj.add_dependencies(jobs, depend_on_jobs)
    return jobs + depend_on_jobs
