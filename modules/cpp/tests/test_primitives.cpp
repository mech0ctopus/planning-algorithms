#include <gtest/gtest.h>
#include <iostream>

#include "optimization/Cost.h"
#include "primitives/Geometry.h"


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
