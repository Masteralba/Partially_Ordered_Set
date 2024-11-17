import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

prime_numbers1 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
prime_numbers = [2, 3, 5, 7, 11, 13, 17]

def are_comparable(x, y):
    return ( ( x % y == 0) or ( y % x == 0) )

def second_is_greater(x, y):
    if are_comparable(x, y):
        return ( y % x == 0)
    
def first_is_greater(x, y):
    if are_comparable(x, y):
        return ( x % y == 0)
    
def find_covering_arr(num):
    covering_arr = []
    for prime in prime_numbers:
        covering_arr.append(prime*num)
    return covering_arr

nodes = set()

edges = []

for i in range(1, 18):
    covering_arr = find_covering_arr(i)
    nodes.add(i)
    nodes.update(set(covering_arr))
    for j in range(len(covering_arr)):
        edges.append((i, covering_arr[j]))


G = nx.Graph()  # создаём объект графа

# определяем список узлов (ID узлов)

# определяем список рёбер
# список кортежей, каждый из которых представляет ребро
# кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром

# добавляем информацию в объект графа
G.add_nodes_from(list(nodes))
G.add_edges_from(edges)

# рисуем граф и отображаем его
pos = graphviz_layout(G, prog="dot")
#nx.draw(G,with_labels=True, font_weight='bold')
nx.draw(G, pos, with_labels=True)
plt.show()