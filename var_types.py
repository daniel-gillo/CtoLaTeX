def init():
    """" Initializer """
    global functions
    global fun
    functions = {}
    fun = ""


def set_function_name(function_name):
    """ Sets the current function we're parsing through. """
    global fun
    if function_name in functions.keys():
        fun = function_name


def function_add(json_ast):
    """ edges that need to be appended at the end of a latex function.
        They are stored in a global list. edge_pop returns these edges
        and clears the list. """
    global functions
    if json_ast["token"] == "function":
        # This has the function name
        function_name = json_ast["right"]["token"]
        functions[function_name] = {}
        # This has the function return type
        functions[function_name]["/*type"] = [json_ast["left"]["token"], True]
    else:
        # If we're here then the ast didn't start with a function header
        # That's very bad, so we're gonna error out
        print("The AST given doesn't begin with a function declaration!")
        raise UnboundLocalError


def variable_add(variable_name, variable_type, function_name=""):
    """ Takes the function name and variable type. Adds that variable's
        type and checks if that conflicts with any other mentions. """
    global functions
    global fun
    # account for the fact we may not know what function we're in
    if function_name == "":
        function_name = fun
    # Check if the function ame is initialized.
    try:
        functions[function_name]
    except KeyError:
        print("You're trying to access a function that isn't initialised!")
        raise KeyError

    if variable_name in functions[function_name].keys():
        # If the variable was already mentioned.
        variable_touch(variable_name, function_name)
        if variable_type != functions[function_name][variable_name][0]:
            # If we're here then the variable name doesn't match the type!
            return "Error"
        else:
            return variable_type
    else:
        # Add the variable type
        functions[function_name][variable_name] = [variable_type, False]
        return variable_type


def variable_get(variable_name, function_name=""):
    """ Fetches the type of a variable name from a function. """
    global functions
    global fun
    # Account for the fact we may not know what function we're in
    if function_name == "":
        function_name = fun
    try:
        return functions[function_name][variable_name][0]
    except KeyError:
        return "Error"


def function_get(function_name=""):
    """ Get the return type of a function. """
    return variable_get("/*type", function_name)


def variable_touch(variable, function=None):
    """ Marks a variable as being used. Touches it like in unix. (kinda) """
    global functions
    global fun
    if not function:
        function = fun
    try:
        functions[function][variable][1] = True
    except KeyError:
        pass


def variable_add_bounds(variable, bounds, function=None):
    """ Adds the bounds for variables. """
    # variable = (lower, upper, inbound)
    global functions
    global fun
    if not function:
        function = fun
    try:
        if len(functions[function][variable]) < 3:
            functions[function][variable].append(bounds)
        else:
            tup = functions[function][variable][2]
            functions[function][variable][2] = (min(tup[0], bounds[0]),
                                                max(tup[1], bounds[1]),
                                                tup[2] or bounds[2])
    except KeyError:
        pass


def variable_return_bounds(variable, function=None):
    """ Returns the variable tuple with the bounds for the variable. """
    # variable = (lower, upper, inbound)
    global functions
    global fun
    if not function:
        function = fun
    try:
        return functions[function][variable][2]
    except KeyError:
        return None


def check_used(function=None):
    """ Checks if all the variables in the register have been used. If function
        isn't used, check all functions. If "/*current" is given, use fun.
        Returns None if all are used, or a list of all that aren't used. """
    global functions
    global fun
    if function == "/*current":
        function = fun
    not_used = []
    for f in functions:
        # If we are only doing a single function, skip all others.
        if function and function != f:
            continue
        for v in functions[f]:
            # Set to True if used.
            if not functions[f][v][1]:
                not_used.append([f, v])
    # We're done iterating through all variables.
    if len(not_used) == 0:
        not_used = None
    return not_used
