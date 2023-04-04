#pragma once
#include <boost/graph/directed_graph.hpp>
#include <boost/graph/graphviz.hpp>

using DirectedGraph=boost::directed_graph<>;
using VertexDescriptor=boost::graph_traits<DirectedGraph>::vertex_descriptor;
