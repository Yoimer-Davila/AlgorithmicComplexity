from graphs import *

labels = ['u', 'v', 'w', 'x', 'y', 'z']
ad_list = NamedMaxFlowMatrix(labels)

ad_list.connect('u', 'v', 10)
ad_list.connect('u', 'x', 7)
ad_list.connect('u', 'w', 4)

ad_list.connect('v', 'y', 2)
ad_list.connect('v', 'z', 6)

ad_list.connect('x', 'v', 2)
ad_list.connect('x', 'y', 10)
ad_list.connect('x', 'w', 2)

ad_list.connect('y', 'z', 7)
ad_list.connect('w', 'y', 2)
ad_list.connect('w', 'z', 10)

source, sink = ad_list.label_index('u'), ad_list.label_index('z')
max_flow, path = ford_fulkerson(ad_list, source, sink)
print(path)
print(max_flow)
show_graph(max_flow_matrix_graph(ad_list, weighted=True, directed=True, layout='circo',  paths=path, labels=labels))


