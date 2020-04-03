from constants import function_declarationRe, function_callRe, array_initializationRe
import re


def is_function_declaration(line):
    return get_func_name(line) is not None


def is_function_call(line):
    m = re.findall(r'(' + function_callRe + ')', line)  # find all matching sub-patterns
    if len(m) > 0:  # if any matching items
        return m[0][1]
    return None


def is_array_initialization(line):
    m = re.findall(r'(' + array_initializationRe + ')', line)  # find all matching sub-patterns
    if len(m) > 0:  # if any matching items
        return True
    return False


def get_id(block_id):
    block_id[0] += 1
    return block_id[0]


def write_instruction(out, block_id):
    out.write('\n/* Block: ' + str(block_id) + ' */\n')
    out.write('if (!resultFuzz.visitedBranchs.contains(' + str(block_id) + '))\n'
                                                                           '\tresultFuzz.visitedBranchs.add(' + str(
        block_id) + ');\n'
              )


def get_func_name(line):
    m = re.findall(r'(' + function_declarationRe + ')', line)  # find all matching sub-patterns
    if len(m) > 0:  # if any matching items
        return m[0][2]
    return None


def new_branch(out, stack, parents, if_branch, block_id, if_block):
    new_id = get_id(block_id)
    write_instruction(out, new_id)
    parents[new_id] = stack[-1]
    if_branch[new_id] = if_block
    stack += [new_id]


def analyze_branches(input_file, out):
    stack = [-1]
    parents = dict()
    functions = dict()
    functions_call = dict()
    if_branch = dict()

    line_n = -1
    for line in input_file:
        line_n += 1
        block_id = [line_n]
        if is_function_declaration(line):
            out.write(line)
            new_branch(out, stack, parents, if_branch, block_id, False)

            func_name = get_func_name(line)
            functions[func_name] = block_id[0]
            continue

        if is_function_call(line):
            func_name = is_function_call(line)
            if func_name not in functions_call:
                functions_call[func_name] = list()
            functions_call[func_name] += [stack[-1]]

        # If there is an array (like {1, 2, 3}) skip the line and don't check for blocks
        if is_array_initialization(line):
            out.write(line)
            continue

        # If there is a class declaration skip the line and don't check for blocks
        if 'class' in line:
            out.write(line)
            continue

        if 'main' in line:
            out.write(line)
            stack.append(0)
            continue

        if_block = False
        if 'if' in line:
            out.write('I.this_branch_id = ' + str(block_id[0] + 1) + ';\n')
            if_block = True

        for c in line:
            out.write(c)

            if c == '{':
                new_branch(out, stack, parents, if_branch, block_id, if_block)

            if c == '}':
                stack.pop()

    for name in functions_call:
        if name not in functions:
            continue
        fun_id = functions[name]
        if len(functions_call[name]) > 1:
            print('multiple parents', fun_id, functions_call[name])
        parent_id = functions_call[name][0]  # assuming only one parent todo: extend this
        parents[fun_id] = parent_id

    return parents, if_branch


def write_graph(out, graph):
    for n in graph[0]:
        out.write('fuzzer.graph.put(' + str(n) + ', ' + str(graph[0][n]) + ');\n')
        print(str(n) + ' -> ' + str(graph[0][n]))

    for n in graph[1]:
        out.write('fuzzer.if_branch.put(' + str(n) + ', ' + ('true' if graph[1][n] else 'false') + ');\n')

    for n in graph[0]:
        out.write('fuzzer.visited_branches.put(' + str(n) + ', false);\n')
