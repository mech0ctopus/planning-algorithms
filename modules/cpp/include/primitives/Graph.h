#pragma once
#include <boost/graph/directed_graph.hpp>
#include <boost/graph/graphviz.hpp>

struct EdgeWeight{
    double weight;
};

template<typename TState>
struct VertexContents {
  std::string name;
  TState value;
};

template<typename T>
using WeightedDirectedGraph=boost::directed_graph<T, EdgeWeight>;
template<typename T>
using VertexDescriptor=typename WeightedDirectedGraph<T>::vertex_descriptor;


template<typename TState>
class StateTransitionGraph {
 public:
  StateTransitionGraph() {}

  VertexDescriptor<TState> add_vertex(const TState& state) {
    return graph_.add_vertex(state);
  }

  void add_edge(VertexDescriptor<TState> source, VertexDescriptor<TState> target, double weight) {
    EdgeWeight edge_weight = { weight };
    graph_.add_edge(source, target, edge_weight);
  }

  void print_vertices() const {
    std::cout << "Vertices:" << std::endl;
    for (const auto& vertex : boost::make_iterator_range(boost::vertices(graph_))) {
      std::cout << graph_[vertex].name << " (value " << graph_[vertex].value << ")" << std::endl;
    }
  }

  void print_edges() const {
    std::cout << "Edges:" << std::endl;
    for (const auto& vertex : boost::make_iterator_range(boost::vertices(graph_))) {
      for (const auto& edge : boost::make_iterator_range(boost::out_edges(vertex, graph_))) {
        VertexDescriptor<TState> target = boost::target(edge, graph_);
        std::cout << graph_[vertex].name << " -> " << graph_[target].name << " (weight " << graph_[edge].weight << ")" << std::endl;
      }
    }
  }

 private:
  WeightedDirectedGraph<TState> graph_;
};