#include <iostream>

#include "primitives/Graph.h"

using StateType=VertexContents<std::string>;
using VertexType=VertexDescriptor<StateType>;


// This problem is defined by Figure 2.8 in LaValle
PlanningProblem<StateType, VertexType> BuildFiveStatePlanningProblem(){
    PlanningProblem<StateType, VertexType> problem;
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

    problem.graph = graph;
    problem.initial_state = a;
    problem.goal_state = d;

    return problem;
}


int main(int argc, char* argv[])
{
    PlanningProblem<StateType, VertexType> problem = BuildFiveStatePlanningProblem();

    std::cout << "State Transition Graph: " << std::endl;
    problem.graph.print_vertices();
    problem.graph.print_edges();

    std::cout << "Initial State: " << std::endl;
    problem.graph.print_vertex(problem.initial_state);
    std::cout << "Goal State: " << std::endl;
    problem.graph.print_vertex(problem.goal_state);

    return 0;
}
