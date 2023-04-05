#include <iostream>

#include "primitives/Graph.h"

using StateType=VertexValue<std::string>;
using VertexType=VertexDescriptor<StateType>;

int main(int,char*[])
{
    StateTransitionGraph<StateType> graph;

    // Add vertices with values
    VertexType v1 = graph.add_vertex(StateType {"v1"});
    VertexType v2 = graph.add_vertex(StateType {"v2"});
    VertexType v3 = graph.add_vertex(StateType {"v3"});

    // Add edges with weights
    graph.add_edge(v1, v2, 1.0);
    graph.add_edge(v2, v3, 2.0);

    // Print vertices and edges
    graph.print_vertices();
    graph.print_edges();

    return 0;
}
