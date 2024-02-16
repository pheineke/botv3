import os
import random
import graphviz



def generate_bdd(filename):
    """
    Generate a Binary Decision Diagram (BDD) with different branches and node types.

    Parameters:
        filename (str): The filename to save the PNG image.

    Returns:
        None
    """
    bdd = graphviz.Digraph(format='png')

    bddvars = ['A','B','C','D','E','F','G']
    varchoice = random.randint(2,len(bddvars)-1)

    lessonvars = bddvars[0:varchoice]

    for node in lessonvars:
        bdd.node(node)

    edges = []
    
    for x in range(2,len(lessonvars)**2):
        node0 = random.choice(lessonvars)
        node1 = random.choice(lessonvars)
        direction = ["a","b","a,b"]
        edge0 = random.choice(direction)
        if (node0,node1,direction[0]) not in edges and (node0,node1,direction[1]) not in edges and (node0,node1,direction[2]) not in edges:
            edges.append((node0,node1,edge0))
            bdd.edge(node0,node1, label=edge0)
    
    # Speichere das BDD als PNG-Datei
    bdd.render(filename, view=False)

try:
    os.remove("./custom_bdd.png")
    os.remove("./custom_bdd.png.png")
except:
    pass