#include <iostream>

#include "primitives/Graph.h"

using StateType=VertexContents<int>;
using VertexType=VertexDescriptor<StateType>;


int main(int argc, char* argv[])
{
    StateTransitionGraph<StateType> graph;

    // Add vertices with values
    VertexType a = graph.add_vertex(StateType {"a", 0});
    VertexType b = graph.add_vertex(StateType {"b", 1});
    VertexType c = graph.add_vertex(StateType {"c", 2});

    // Add edges with weights
    graph.add_edge(a, b, 1.0);
    graph.add_edge(b, c, 2.0);

    // Print vertices and edges
    graph.print_vertices();
    graph.print_edges();

    return 0;
}
