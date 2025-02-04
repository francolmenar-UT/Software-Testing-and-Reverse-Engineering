def if_stack_pop(input_file, out):
    stack = []

    skip_next = False
    stack_pop_string = 'I.stack.pop();\n'

    bracket_in_previous_line = False

    for line in input_file:
        if 'if' in line:
            fi = True
        else:
            fi = False

        # write before throwing the exception
        if 'throw new' in line or 'return' in line:
            if bracket_in_previous_line:
                out.write(stack_pop_string)
            out.write(line)
            skip_next = True
            continue

        bracket_in_previous_line = False
        for c in line:
            if c == '{':
                stack += [fi]
                bracket_in_previous_line = True
            if c == '}':
                v = stack.pop()
                if v and not skip_next:
                    out.write(stack_pop_string)
                skip_next = False
            out.write(c)
