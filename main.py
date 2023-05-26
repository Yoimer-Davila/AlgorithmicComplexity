from graphs import NamedAdjacencyList, show_graph, adjacency_list_graph, from_kruskal, kruskal, breadth_first_search_al

labels = ['5to', 'Practicas', 'Diplomado', 'ChatGPT', 'Back', 'Front', 'Seguridad', 'QA', 'Gestion']
ad_list = NamedAdjacencyList(labels, True)

ad_list.connect('5to', 'ChatGPT', 2, True)
ad_list.connect('5to', 'Diplomado', 10, True)
ad_list.connect('5to', 'Practicas', 5, True)

ad_list.connect('Practicas', 'Seguridad', 7, True)
ad_list.connect('Practicas', 'Front', 2, True)
ad_list.connect('Practicas', 'Gestion', 10, True)
ad_list.connect('Practicas', 'Back', 3, True)
ad_list.connect('Practicas', 'Diplomado', 5, True)

ad_list.connect('Diplomado', 'ChatGPT', 10, True)

ad_list.connect('Diplomado', 'Front', 4, True)
ad_list.connect('Diplomado', 'Back', 4, True)
ad_list.connect('Diplomado', 'Seguridad', 2, True)
ad_list.connect('Diplomado', 'Gestion', 3, True)
ad_list.connect('Diplomado', 'QA', 2, True)

ad_list.connect('Back', 'Front', 1, True)
ad_list.connect('Back', 'Seguridad', 3, True)

ad_list.add_node('Back')


print(ad_list)

min_ad_list = kruskal(ad_list)
path = breadth_first_search_al(from_kruskal(len(ad_list), min_ad_list), 0)
print(path)
graph = adjacency_list_graph(ad_list, weighted=True, path=path, labels=ad_list.labels(), layout='circo')
show_graph(graph)


