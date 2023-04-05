#include <iostream>

#include "primitives/Graph.h"

using StateType=VertexContents<std::string>;
using VertexType=VertexDescriptor<StateType>;

// This graph is defined by Figure 2.8 in LaValle
StateTransitionGraph<StateType> BuildFiveStateGraph(){
    StateTransitionGraph<StateType> graph;

    // Add vertices with values
    VertexType a = graph.add_vertex(StateType {"a", "a"});
    VertexType b = graph.add_vertex(StateType {"b", "b"});
    VertexType c = graph.add_vertex(StateType {"c", "c"});
    VertexType d = graph.add_vertex(StateType {"d", "d"});
    VertexType e = graph.add_vertex(StateType {"e", "e"});

    // Add edges with weights
    graph.add_edge(a, a, 2.0);
    graph.add_edge(a, b, 2.0);
    graph.add_edge(b, d, 4.0);
    graph.add_edge(b, c, 1.0);
    graph.add_edge(c, a, 1.0);
    graph.add_edge(c, d, 1.0);
    graph.add_edge(d, c, 1.0);
    graph.add_edge(d, e, 1.0);

    return graph;
}


int main(int argc, char* argv[])
{
    StateTransitionGraph<StateType> graph = BuildFiveStateGraph();

    graph.print_vertices();
    graph.print_edges();

    return 0;
}
