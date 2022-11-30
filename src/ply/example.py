def p_global_assign_const_statement(p):
    """global_const_assign_statement : KCONST ID type assign_expr"""
    # redeclared check
    if p[2] in global_names:
        print(f"Error: {p[2]} redeclared in the scope")
        return

    t = type(p[4])
    if p[3] == 'bool':
        if p[4] is not None:
            if t != bool:
                print("TypeError: non bool type assigned to bool")
            else:
                global_names[p[2]] = p[4]  # Accepted

        else:
            global_names[p[2]] = False  # zero accepted

    elif p[3] == 'int':
        if p[4] is not None:
            if t != int:
                print("TypeError: non int type assigned to int")
            elif p[4] > (1>>63-1) or p[4] <= (-1<<64):
                error_list.append(f"Overflow Error: can not use {p[4]} for int32")
            else:
                global_names[p[2]] = p[4]  # Accepted

        else:
            global_names[p[2]] = 0  # zero accepted

    elif p[3] == 'string':
        if p[4] is not None:
            if t != str:
                print("TypeError: non string type assigned to string")
            else:
                global_names[p[2]] = p[4]  # Accepted

        else:
            global_names[p[2]] = ""  # zero accepted

    global_constants.add(p[2])
    p[0] = ("global constant", p[2], p[3], p[4])