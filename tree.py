import back
import edges
import re
import types


class Tree:
    def __init__(self, type, id, indent=0, parent=None, next=None):
        if type.lower() in ["function", "code", "if", "else if", "else",
                            "while", "error", "return"]:
            self.type = type.lower()
        else:
            print("You need to assign this node a correct type.")
            print('Must be: "function", "code", "if", "else if", "else", '
                  '"while", "error", "return"')
            raise TypeError
        self.id = id
        self.indent = indent
        self.parent = parent
        self.next = next
        self.parameters = None
        self.code = None
        self.error = None
        self.other_ifs = None
        self.condition = None

    def __str__(self):
        """ Generate's a string representation of the node and it's node
            friends. It will do this in latex, so node friends move up a
            dimension to 2D! """

        # Old print code from before thr latex conversion
        ind = "    "
        # nx = ""
        # cod = ""
        # cond = ""
        # param = ""
        # others = ""
        # parent = ""
        # if self.other_ifs:
        #     for i in self.other_ifs:
        #         others += str(i)
        # if self.parameters:
        #     param = "( Param " + str(self.parameters) + " )\n" + ind
        # if self.condition:
        #     cond = "( Cond: " + str(self.condition) + " )\n" + ind
        # if self.code:
        #     cod = "Code: \"<" + str(self.code) + ">\""
        # if self.next:
        #     nx = str(self.next)

        # The different types of nodes have different latex code representation
        # in latex. So we'll have to use cases to set the middle code.
        header = ""
        footer = ""
        parent_string = ""
        if self.parent:
            parent_string = str(self.parent.getId())

        # add the function headers
        if self.type == "function":
            color = back.backend.color_pick()
            header = "\generateBlockStyles{" + color + "}\n\\begin{tikzpict" \
                     "ure}[node distance = 1cm and 1cm]\n    \\begin{scope}" \
                     "[layered layout, sibling distance=25mm, every edge/.s" \
                     "tyle={draw=black}]\n"
            footer = "    \\end{scope}\n\\end{tikzpicture}\n"
        # Check if we're part of a true if branch
        else:
            if self.parent.getType() in ["if"] and \
                    (self in self.parent.getOtherIf() or
                             self.parent.getCode() == self):
                # This means we're the first node inside and if branch
                parent_string += "I"
            # elif self.parent.getType() in ["if"] and \
            #                 self.parent.getNext() == self:
            #     # This means we're the first node following an if branch
            #     parent_string = "F" + parent_string
            elif self.parent.getType() == "while" and \
                            self.parent.getCode() == self:
                # This means we're the first node inside and if branch
                parent_string += "W"
                # elif self.parent.getType()  == "while" and \
                #                 self.parent.getNext() == self:
                #     # This means we're the first node following an if branch
                #     parent_string = "Fcond" + parent_string

        latex_code = ind * 2
        if self.type == "function":
            latex_code += "% This is a main function. It's called " + \
                          self.code + "\n"
            latex_code += ind * 2 + "\\funcDec{" + str(self.id) + "}{Params: " + \
                          re.sub("[\[\]\"]", "", str(self.parameters[1:])) + \
                          "}{Function: " +  self.code  + "}\n"
        elif self.type == "code":
            latex_code += "% This is a code line\n"
            latex_code += ind * 2 + "\\operationDec{" + str(
                self.id) + "}{" + self.code + "}{" + parent_string + "}\n"
        elif self.type == "error":
            latex_code += "% This is an error line\n"
            latex_code += ind * 2 + "\\errorDec{" + str(
                self.id) + "}{" + self.code + "}{" + parent_string + "}\n"
        elif self.type == "if":
            latex_code += "% This is an if statement. It's id is " + str(
                self.id) + "\n"
            latex_code += ind * 2 + "\\genericCond{" + str(
                self.id) + "}{" + "Condition" + "}{" + parent_string + "}\n"
            latex_code += ind * 2 + "\\operationDec{" + str(
                self.id) + "I}{" + "If " + self.condition + \
                          "}{" + str(self.id) + "}\n"
        elif self.type == "else if":
            latex_code += "% This is an else if statement. It's id is " + str(
                self.id) + "\n"
            latex_code += ind * 2 + "\\genericCond{" + str(
                self.id) + "}{" + "If " + self.condition + \
                          "}{" + parent_string + "}\n"
        elif self.type == "else":
            latex_code += "% This is an else statement. It's id is " + str(
                self.id) + "\n"
            latex_code += ind * 2 + "\\operationDec{" + str(
                self.id) + "}{" + "Else" + "}{" + parent_string + "}\n"
        elif self.type == "while":
            latex_code += "% This is a while loop. It's id is " + str(
                self.id) + "\n"
            latex_code += ind * 2 + "\\whileDec{" + str(
                self.id) + "}{while}{" + parent_string + "}\n"
            latex_code += ind * 2 + "\\operationDec{" + str(
                self.id) + "W}{" + self.condition + "}{" + str(
                self.id) + "}\n"
        elif self.type == "return":
            latex_code += "% This is a return statement. It's id is " + str(
                self.id) + "\n"
            latex_code += ind * 2 + "\\funcConc{" + str(
                self.id) + "}{" + self.code + "}{" + parent_string + "}\n"
        else:
            print("We shouldn't be here. Tree print")
            raise UnboundLocalError

        # Call next node and other ifs
        nx = ""
        err = ""
        code = ""
        others = ""
        backtrack = ""
        if self.other_ifs:
            for i in self.other_ifs:
                others += str(i)
        if self.type in ["if", "else if", "else", "while"] and self.code:
            code = str(self.code)
        if self.next:
            nx = str(self.next)
        if self.error:
            err = str(self.getError())
        # If we're last, get edge in case we're in an if / while
        elif self.indent > 1 and self.type != "error":
            last = self.find_last()
            for l in last:
                e = ind * 2 + "% This is an edge. It connects end nodes.\n"
                e += ind * 2 + "\\edgeDraw{" + str(self.id) + "}{" + l + "}\n"
                # S tore edge code in global var in back.py master instance.
                edges.edge_add(e)

        # Put all of the edges to footer here
        if self.type == "function":
            t_footer = ind * 2 + "% This is the function footer. It has the " \
                               "return type.\n"
            # The idiot plan is: Regex to find the id of the return node from
            # the latex code we made. Increment that, by a lot.
            last_id = re.search(r"        \\operationDec{(\d+)}{End of "
                                r"Function}{\d+}", nx)
            last_id = last_id.group(1)
            footer_id = str((1000000 + int(last_id) )<< 1)
            t_footer += ind * 2 + "\\ellipseDec{" + footer_id + "}{Return Type: " + \
                      self.parameters[0] + "}{" + last_id + "}\n"
            footer = t_footer + edges.edge_pop() + "\n" + footer

        return header + latex_code + backtrack + err + code + others + nx + \
               footer
        # return "\n"+ind + self.type + str(self.id) + " " + cond  + param +
        #  cod + others + nx

    def find_last(self):
        """ Goes through all parents to find if the node is in a if or while.
            Returns that if or while's next node. Continues to that's parent
            until it finds a next. Or returns empty string if there is none."""
        ast = self
        ind = self.indent
        while ast.getIndent() > 0:
            parent = ast.getParent()
            if parent.getIndent() == ind:
                ast = parent
                continue
            if parent.getType() == "if" and parent.getNext():
                return [str(parent.getNext().getId())]
            elif parent.getType() == "while":
                return [str(parent.getId()), str(parent.getNext().getId())]
            ast = parent
        return None

    def append(self, end_node, message):
        """ Add a code noe with a message to the end
            of a function. """
        if self.type == "function":
            node = self
            while node.getNext() is not None:
                node = node.getNext()
            node.setNext(end_node)
            node.getNext().setCode(message)

    def getType(self):
        return self.type

    def getIndent(self):
        return self.indent

    def getParent(self):
        return self.parent

    def getNext(self):
        return self.next

    def getCode(self):
        return self.code

    def getError(self):
        return self.error

    def getId(self):
        return self.id

    def getCondition(self):
        if self.type in ["if", "else if", "while"]:
            return self.condition
        else:
            return None

    def getOtherIf(self):
        if self.type in ["if", "else if"] and self.other_ifs is not None:
            return self.other_ifs
        else:
            return [None]

    def getParameter(self):
        if self.type in ["function"]:
            return self.parameters
        else:
            return None

    def getType(self):
        return self.type

    # Set commands
    def setIndent(self, indent):
        self.indent = indent

    def setParent(self, parent):
        self.parent = parent

    def setNext(self, next):
        self.next = next

    def setCode(self, code):
        self.code = code

    def setError(self, e):
        if e.getType() == "error":
            self.error = e
        else:
            print(
                "You need to set an error type node to be the error of a "
                "normal node!")
            raise TypeError

    def setCondition(self, condition):
        if self.type in ["if", "else if", "while"]:
            self.condition = condition

    def addOtherIf(self, other):
        if self.type in ["if", "else if"]:
            if self.other_ifs is None:
                self.other_ifs = []
            if type(other) is Tree:
                self.other_ifs.append(other)
            elif type(other) == type([]):
                self.other_ifs.extend(other)
            else:
                print("Other_If error. You're appending not a tree object!")
                print(other)
                raise TypeError

    def addParameter(self, param):
        if param is None:
            pass
        elif self.type in ["function"]:
            if self.parameters is None:
                self.parameters = []
            if type(param) == type(""):
                self.parameters.append(param)
            elif type(param) == type([]):
                self.parameters.extend(param)
            else:
                print("AppParamter error. input needs to be str or list.")
                raise TypeError
