
def init():
    """" Initializer """
    global edges
    edges = []


def edge_add(code):
    """ edges that need to be appended at the end of a latex function.
        They are stored in a global list. edge_pop returns these edges
        and clears the list. """
    global edges
    edges.append(code)


def edge_pop():
    """ Returns all edges stored in global var edges. it concats
        all of the code and returns a string.
        See def edge_add to add edges to the golobal var. """
    global edges
    pop = ""
    for e in edges:
        pop += e
    edges = []
    return pop
