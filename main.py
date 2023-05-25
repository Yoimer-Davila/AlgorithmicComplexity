from graphs import from_adjacency_file, show_graph, adjacency_list_graph, from_kruskal, kruskal, breadth_first_search_al

ad_list, labels = from_adjacency_file("list.adjl", weighted=True, has_labels=True)

min_ad_list = kruskal(ad_list)
path = breadth_first_search_al(from_kruskal(len(ad_list), min_ad_list), 0)
print(path)
graph = adjacency_list_graph(ad_list, weighted=True, path=path, labels=labels)
show_graph(graph, size='10px,3px')


