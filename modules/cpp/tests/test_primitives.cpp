#include "gtest/gtest.h"
#include "GeometryTypes.h"
#include <iostream>

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

// This is just for testing. It returns the same state as before
template<typename TState, typename TAction>
TState arbitraryTransitionFunc(const TState& state, const TAction& action){
  return state;
}

TEST(poseType, InitializationWorks) {
  Pose arbitraryPose;
  arbitraryPose.point = {0.,0.,0.};
  arbitraryPose.orientation = {0.,0.,0.,1.};
}

TEST(costFunctional, CalculatesCostCorrectly) {
  // Define an arbitrary initial state
  Pose initialPose;
  initialPose.point = {0.,0.,0.};
  initialPose.orientation = {0.,0.,0.,1.};

  // Build an arbitrary plan (sequence of actions)
  std::vector<Twist2d> arbitaryPlan{};
  arbitaryPlan.push_back({1.0, 0.}); // u_1
  arbitaryPlan.push_back({0.5, 0.}); // u_2
  arbitaryPlan.push_back({0.2, 0.}); // u_3

  double cost = calculateCostFunctional<Pose, Twist2d>(arbitaryPlan,
                                                       arbitraryTransitionFunc<Pose, Twist2d>,
                                                       initialPose);
  std::cout << "Expected Cost: " << arbitaryPlan.size() << ", Actual Cost: " << cost << std::endl;
  ASSERT_EQ(cost, arbitaryPlan.size());
}

int main(int argc, char **argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
