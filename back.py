import json
import operator
import math
import random
import re
import sys
import edges
import tree
import var_types


class backend:
    def main(filename, out):
        """ This is the glorious main function. It's the best of all the main
            functions. It's so main we need this function for everything.
            Right now it reads piped-in JSON strings. All the strings. No
            string is too big. And then, it converts JSON to variables.
            All of them, into an AST. The best AST god ever created. Then the
            function prints the AST. In the best display of printing ever
            witnessed by man. The best ever. """
        global id_count
        id_count = 0
        edges.init()
        var_types.init()
        asts = []
        # SProperly randomised colours now!
        random.seed()
        # print(filename)
        # if "\n" in filename:
        # raw_data = filename.split("\n")
        # else:
        with open(filename, "r") as fp:
            raw_data = fp.readlines()
        # This if-statement is needed because if the json file contains more
        # than one json object the first line of just "\n" isn't ignored.
        if raw_data[0] == "\n":
            raw_data = raw_data[1:]
        # Turn the list of .jsons into variables
        for j in raw_data:
            if j[0] == "\n":
                continue
            jay = re.sub("}{", "},{", j)
            jay = "[" + jay + "]"
            # If this fails it's because we're printing a yacc error line
            try:
                asts.extend(json.loads(jay))
            except:
                print("Yacc encountered a syntax error with your code!")
                print(j[1:])
                raise ImportError

        # Add the functions to the types class
        for ast in asts:
            var_types.function_add(ast)

        # Process the asts one a time
        latex_main = ""
        for ast in asts:
            # print(ast)
            # print(backend.ast_print(ast))
            t = backend.traverse(ast, 0)
            t.append(tree.Tree("code", id_count, 1), "End of Function")
            id_count += 1
            # Unused us a list of [function name, variable name] tuples lists.
            unused = var_types.check_used("/*current")
            if unused:
                message = "Unused Variables:\n"
                for v in unused:
                    message += v[1] + ", "
                t.append(tree.Tree("code", id_count, 1), message[:-2])
                id_count += 1
            backend.parent_traverse(t)
            latex_main += str(t)

        # Remove "^" from before numbers
        latex_main = re.sub("\^", "", latex_main)
        # Replace underscore with \_ for latex stuff
        latex_main = re.sub("_", "\\_", latex_main)
        # Replace "number unary-" with -number
        latex_main = re.sub("(\d+.?\d*) unary-", "-\\1", latex_main)

        # SInce we have our nice tree representation we can print that to latex
        with open("header.tex", "r") as fp:
            latex_header = fp.read()
        with open("footer.tex", "r") as fp:
            latex_footer = fp.read()
        # print(latex_header)
        # print(latex_main)
        # print(latex_footer)
        #
        # print(out)
        with open(out, "w+") as out_fp:
            out_fp.write(latex_header)
            out_fp.write(latex_main)
            out_fp.write(latex_footer)

    def traverse(ast, indent):
        """ This function traverses recursively through the dict based on
            the .json file that the main function read.
            It returns a Tree object that represents all the code. """

        # The obvious choice first.
        global id_count
        if ast is None:
            return None
        if ast["token"] == "ifBodyExt":
            ast = ast["left"]
        # If this is the main function header node
        if ast["token"] == "function":
            node = tree.Tree("function", id_count, indent)
            id_count += 1
            var_types.set_function_name(ast["right"]["token"])
            # Return type is first parameter
            node.addParameter(ast["left"]["token"])  # Matt doesn't want this
            # Check to see if params are listed
            try:  # account for [right][left][left] being none
                node.addParameter(backend.param_to_list(ast["right"]["left"]
                                                        ["left"]))
            except TypeError:
                pass
            # Code in this case will hold the function name
            node.setCode(ast["right"]["token"])
            # Recursive Call, set that to the next node.
            node.setNext(backend.traverse(ast["right"]["right"],  # ["right"]
                                          indent + 1))

        # If the next feature is a line of normal code
        elif ast["token"] == "bodyCode":

            if ast["left"]["token"] == "if":
                node = tree.Tree("if", id_count, indent)
                id_count += 1
                node.setCondition(backend.bodyCode_traverse(ast["left"]
                                                            ["left"]))
                backend.lookAtBody(ast["left"]["left"], node)
                node = backend.dead_code_checker(node, ast["left"]["left"],
                                                 indent)
                # If there is an else-if / else coming up
                if ast["left"]["right"]["token"] == "ifBodyExt":
                    if not ast["left"]["right"]["right"] is None:
                        node.setCode(backend.traverse(ast["left"]["right"]
                                                      ["left"], indent + 1))
                        node.addOtherIf(backend.if_handler(ast["left"]["right"]
                                                           ["right"], indent))
                    if ast["left"]["right"]["left"] is not None:
                        node.setCode(backend.traverse(ast["left"]["right"],
                                                      indent + 1))

                else:
                    node.setCode(backend.traverse(ast["left"]["right"],
                                                  indent + 1))
                node.setNext(backend.traverse(ast["right"], indent))

            # If we're dealing with a return statement
            elif ast["left"]["token"] == "return":
                node = tree.Tree("return", id_count, indent)
                id_count += 1
                node.setCode(backend.bodyCode_traverse(ast["left"]["left"]))
                backend.lookAtBody(ast["left"]["left"], node)
                node.setNext(backend.traverse(ast["right"], indent))

            # While loop
            elif ast["left"]["token"] == "loop":
                node = tree.Tree("while", id_count, indent)
                id_count += 1
                node.setCondition(backend.bodyCode_traverse(ast["left"]
                                                            ["left"]))
                backend.lookAtBody(ast["left"]["left"], node)
                node = backend.dead_code_checker(node, ast["left"]["left"],
                                                 indent)
                node.setCode(backend.traverse(ast["left"]["right"],
                                              indent + 1))
                node.setNext(backend.traverse(ast["right"], indent))

            else:
                # Left contains the current line, right the next.
                node = tree.Tree("code", id_count, indent)
                id_count += 1
                # BodyCode traverse, traverses through an ast & returns a
                # string.
                node.setCode(backend.bodyCode_traverse(ast["left"]))
                backend.lookAtBody(ast["left"], node)
                node.setNext(backend.traverse(ast["right"], indent))

        # If the next feature is an else_if-statement
        # elif ast["token"] == "elseif":
        #    temp_ast = ast
        #    while True:
        else:
            pass
            # print(backend.ast_print(ast))
        return node

    def if_handler(ast, indent):
        """ Handles what happens when we encounter an if-statement.
            This function exists because this handling can occur in
            sub-nodes of two different parent nodes. """
        all_else = []
        global id_count
        # print(backend.ast_print(ast))
        while ast is not None:
            # print(type(ast))
            if ast["token"] == "else":
                node = tree.Tree("else", id_count, indent)
                id_count += 1
                node.setCode(backend.traverse(ast["left"], indent + 1))
                all_else.append(node)
                break
            elif ast["token"] == "elseif":
                node = tree.Tree("else if", id_count, indent)
                id_count += 1
                node.setCondition(backend.bodyCode_traverse(ast["left"]
                                                            ["left"]))
                backend.lookAtBody(ast["left"]["left"], node)
                node = backend.dead_code_checker(node, ast["left"]["left"],
                                                 indent)
                if ast["left"]["right"]["token"] == "ifBodyExt":
                    node.setCode(backend.traverse(ast["left"]["right"]["left"],
                                                  indent + 1))
                    all_else.append(node)
                    ast = ast["left"]["right"]["right"]
                else:
                    node.setCode(backend.traverse(ast["left"]["right"],
                                                  indent + 1))
                    break
            else:
                print("We shouldn't be here in if_handler.")
                print(ast)
                raise UnboundLocalError

        return all_else

    def dead_code_checker(node, ast, indent):
        """ Checks if the ast condition given to it, can succeed.
            Returns the node with an error node attached if there is dead
            code. """
        global id_count
        # We are gonna run findBounds twice on this, but screw it.
        possible = backend.findBounds(ast)
        possible = possible[2]
        if not possible:  # Ha ha ha
            # Gonna make an error node, since this if statement is dead code.
            e = tree.Tree("error", id_count, indent)
            id_count += 1
            e.setCode("Dead Code Inside!")
            node.setError(e)
        return node

    def findBounds(ast):
        """ Return the bounds of an ast and whether its
            possible for a value tob be within them. """
        # http://stackoverflow.com/questions/1740726/python-turn-string-into
        # -operator
        ops = {"+": operator.add, "-": operator.sub, "/": operator.truediv,
               "*": operator.mul, "%": operator.mod}
        token = ast["token"]
        if token == "functionCall":
            return (-math.inf, math.inf, True)
        elif token in ["!=", "==", "and", "or"]:
            left = list(backend.findBounds(ast["left"]))
            right = list(backend.findBounds(ast["right"]))
            inBounds = left[2] or right[2]
            if left[0] > right[1] or left[1] < right[0]:
                inBounds = False
            return (0, 1, inBounds)
        elif token in ["<", "<="]:
            # check if it is possible to have the left less then the right
            left = list(backend.findBounds(ast["left"]))
            right = list(backend.findBounds(ast["right"]))
            inBounds = left[2] or right[2]
            # if the lower bound of the left is a constant greater then the
            # upper bound of the right then can never be true
            if left[0] > right[1]:
                inBounds = False
            return (0, 1, inBounds)
        elif token in [">", ">="]:
            left = list(backend.findBounds(ast["left"]))
            right = list(backend.findBounds(ast["right"]))
            inBounds = True
            # if the lower bound of the right is greater then the lower bound
            # of the right this statement can never be true
            if left[1] < right[0]:
                inBounds = False
            return (0, 1, inBounds)
        elif token in ["--", "++", "deref", "unary+", "unary-"]:
            return backend.findBounds(ast["left"])
        elif token in ["*", "%", "-", "+", "/"]:
            left = list(backend.findBounds(ast["left"]))
            right = list(backend.findBounds(ast["right"]))
            curLeft = -math.inf
            curRight = math.inf
            if left[0] != math.inf and right[0] != math.inf:
                curLeft = ops[token](left[0], right[0])
            if left[1] != math.inf and right[1] != math.inf:
                curRight = ops[token](left[1], right[1])
            return (curLeft, curRight, left[2] or right[2])
        elif token == "getAddr":
            return (-math.inf, math.inf, True)
        elif token == "sizeof":
            return (0, math.inf, True)
            # retrieve floats and ints
        elif re.search("\^\d+.\d+", token):
            fval = float(token[1:])
            return (fval, fval, True)
        elif re.search("\^\d+", token):
            ival = int(token[1:])
            return (ival, ival, True)
        # retrieve the bounds of a variable
        else:
            return var_types.variable_return_bounds(ast["token"])

    def lookAtBody(ast, node):
        """ Goes through the ast code line. If there is a type error
            append an error node to the node we're checking. """
        global id_count
        backend.usedVars(ast)
        e = ""
        if ast["token"] == "=":
            logic = backend.generateLogic(ast["right"])
            if ast["left"]["left"] is not None:
                if ast["left"]["left"]["token"] != logic:
                    e = "Error! Type Mismatch!"
                elif (var_types.variable_get(ast["left"]["token"]) != "Error"):
                    e = "Error! Variable already initiated"
                else:
                    e = var_types.variable_add(ast["left"]["token"], logic)
                    var_types.variable_add_bounds(ast["left"]["token"],
                                                  backend.findBounds(
                                                      ast["right"]))
            else:
                e = var_types.variable_get(ast["left"]["token"])
                if not e.startswith("Error"):
                    e = var_types.variable_add(ast["left"]["token"], logic)
                    var_types.variable_add_bounds(ast["left"]["token"],
                                                  backend.findBounds(
                                                      ast["right"]))
        else:
            e = backend.generateLogic(ast)
        if e.startswith("Error"):
            # We have an error, need to make an error node
            # The 1 indentation is arbitrary
            t = tree.Tree("error", id_count, 1)
            if e == "Error":
                t.setCode("Error! Type Mismatch!")
            else:
                t.setCode(e)
            id_count += 1
            # Set the e node as error to "node" node.
            node.setError(t)

    def generateLogic(ast):
        """ Recursively goes through ast.
            Returns type of a single line of code. """
        if ast is None:
            return True
        if ast["token"] == "functionCall":
            funcName = ast["left"]["token"]
            param = ast["right"]
            var_types.variable_touch(param["token"])
            while param["left"] is not None:
                param = param["left"]
                var_types.variable_touch(param["token"])
            return var_types.function_get(funcName)
        elif ast["token"] in [">", "<", ">=", "<=", "!=", "==", "sizeof",
                              "and", "or", "getAddr"]:
            if backend.generateLogic(ast["left"]) != "Error" and \
                            backend.generateLogic(ast["right"]) != "Error":
                return "int"
            else:
                return "Error"
        elif ast["token"] in ["--", "++", "deref", "unary+", "unary-"]:
            return backend.generateLogic(ast["left"])
        elif ast["token"] in ["*", "+", "%", "-", "+", "/"]:
            left = backend.generateLogic(ast["left"])
            right = backend.generateLogic(ast["right"])
            if (left == "Error" or right == "Error"):
                return "Error"
            elif left == "float" or right == "float":
                return "float"
            else:
                return "int"
        elif re.search("\^\d+.\d+", ast["token"]):
            return "float"
        elif re.search("\^\d+", ast["token"]):
            return "int"
        else:
            return var_types.variable_get(ast["token"])

    def parent_traverse(t, parent=None):
        """ Set the parent nodes in the tree """
        if not type(t) is tree.Tree:
            pass
        else:
            t.setParent(parent)
            backend.parent_traverse(t.getNext(), t)
            backend.parent_traverse(t.getCode(), t)
            backend.parent_traverse(t.getCondition(), t)
            backend.parent_traverse(t.getParameter(), t)
            backend.parent_traverse(t.getError(), t)
            ifs = t.getOtherIf()
            if ifs is not None:
                prev = t
                for i in ifs:
                    backend.parent_traverse(i, prev)
                    prev = i

    def param_to_list(ast):
        """ Goes through the parameters of the ast and
            returns all the values in  a list. """
        params = []
        while ast is not None:
            # Append [var_name, var_type]
            params.append(ast["token"])
            # params.append(ast["right"]["token"]) # Matt doesn't want this.
            # Add the variables to the main type checker
            var_types.variable_add(ast["token"], ast["right"]["token"])
            var_types.variable_add_bounds(ast["token"],
                                          (-float('inf'), float('inf'), True))
            ast = ast["left"]
        return params

    def ast_print(ast, indent=0):
        """ Print the JSON ast, in a way that's legible.
            Returns that string. """
        if ast is None:
            return indent * "  " + "None"
        if type(ast) == type(""):
            return indent * "  " + ast

        s = "  " * indent
        l1 = s + "Token: " + str(ast["token"]) + "\n"
        l2 = s + "Left: \n" + str(backend.ast_print(ast["left"],
                                                    indent + 1)) + "\n"
        l3 = s + "Right: \n" + str(backend.ast_print(ast["right"],
                                                     indent + 1)) + "\n"
        return l1 + l2 + l3

    def color_pick():
        """ Returns a random LaTex color for the functions. """
        colors = ["green", "blue", "cyan", "magenta", "yellow", "brown",
                  "lime",  # "red", "darkgray", "lightgray", "black", "gray",
                  "olive", "orange", "pink", "purple", "teal", "violet"]
        return random.choice(colors)

    def usedVars(ast):
        """ Checks all variables in an ast and calls on
            var_types.variable_touch to mark these as used. """
        if ast is None:
            pass
        else:
            if re.search("\w+", ast["token"]):
                var_types.variable_touch(ast["token"])
            backend.usedVars(ast["left"])
            backend.usedVars(ast["right"])

    def bodyCode_traverse(ast):
        """ This function goes through a BodyCode node and it's children.
            It traverses through them and returns a string of the entire
            expression. """
        if ast is None:
            return ""
        elif type(ast) == type(""):
            return ast
        return backend.bodyCode_traverse(ast["left"]) + " " + \
           backend.bodyCode_traverse(ast["token"]) + " " + \
           backend.bodyCode_traverse(ast["right"])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("You need to supply a JSON file! and output file!")
        sys.exit()

    json_filename = sys.argv[1]
    output_file = sys.argv[2]
    backend.main(json_filename, output_file)
