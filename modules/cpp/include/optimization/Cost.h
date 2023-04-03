#pragma once
#include <functional>
#include <vector>


/*
/ Calculates a single cost term for a given state/action pair.
*/
template<typename TState, typename TAction>
double calculateCostTerm(const TState& state, const TAction& action){
  // TODO: Actually calculate cost here.
  return 1.;
}


/*
/ Calculates stage-additive cost (or loss) functional for a K-step plan.
/ 
/ plan: A sequence of k actions.
/ stateTransition: A callable state transition function.
/ initialState: The initial State of the system.
*/
template<typename TState, typename TAction>
double calculateCostFunctional(const std::vector<TAction>& plan,
                               const std::function<TState(TState, TAction)>& stateTransition,
                               const TState& initialState){
  // Calculate cost terms
  auto costTerms{0.};
  TState currentState{initialState};
  for (auto action : plan){
    // Calculate new current state
    currentState = stateTransition(currentState, action);
    costTerms += calculateCostTerm<TState, TAction>(currentState, action);
  }

  // TODO: Make use of final state
  // Calculate final term
  auto finalTerm = 0. ;

  return costTerms + finalTerm;
}
