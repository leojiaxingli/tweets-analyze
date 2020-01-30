import networkx as nx
import matplotlib.pyplot as plt
import json
import os
from prettytable import PrettyTable
def get_followers(name):
    f = open("{}.json".format(name), encoding='utf-8')
    content = f.read()
    fol = json.loads(content)
    return fol
def get_network(ego):
    G = nx.Graph()
    G.add_node(ego)
    initlal_fol = get_followers(ego)
    for fol in initlal_fol:
        G.add_node(fol)
        G.add_edge(fol,ego)
        #"netjson//AdrienKumar2"
    for root, dirs, files in os.walk("netjson"):
        for f in files:
            user = os.path.splitext(f)[0]
            G.add_node(user)
            G.add_edge(user,ego)
            fol_of_fol = get_followers("netjson//{}".format(user))
            for fol in fol_of_fol:
                G.add_node(fol)
                G.add_edge(fol,user)
    rmlist = []
    for n in G.nodes:
        if G.degree(n)==1:
            rmlist.append(n)
    for n in rmlist:
        G.remove_node(n)
    """keeplist = []
    for n in G.nodes:
        keeplist.append(n)
    with open('acc.json', 'w+') as outfile:
        json.dump(keeplist, outfile)"""

    table = PrettyTable(["Property", "Value"])
    table.add_row(["Number of nodes:", G.number_of_nodes()])
    table.add_row(["Number of edges:", G.number_of_edges()])
    table.add_row(["Density:", round(nx.density(G),4)])
    table.add_row(["Average path length: ", round(nx.average_shortest_path_length(G),4)])
    table.add_row(["Diameter:", nx.diameter(G)])
    table.add_row(["Average in-degree/out-degree:", round(G.number_of_edges() / G.number_of_nodes(),4)])
    print(table)

    nx.draw(G, with_labels= True)
    plt.draw()
    plt.show()


    DEG = []
    for i in G.nodes:
        deg = (G.degree(i))
        DEG.append(deg)
    X = range(1,max(DEG)+1)
    Y = []
    for i in X:
        y = DEG.count(i)
        Y.append(y)
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of Nodes")
    plt.plot(X, Y)
    plt.show()
