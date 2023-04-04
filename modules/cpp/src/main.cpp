#include <iostream>

#include "primitives/Graph.h"

int main(int,char*[])
{
    // TODO: Consider using `directed_graph` vs. `adjacency_list`
    DirectedGraph g;
    VertexDescriptor v0 = g.add_vertex();
    VertexDescriptor v1 = g.add_vertex();
    g.add_edge(v0, v1);

    write_graphviz(std::cout, g);

    return 0;
}
