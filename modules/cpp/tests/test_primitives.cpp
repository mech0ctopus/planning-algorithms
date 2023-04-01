#include "gtest/gtest.h"
#include "GeometryTypes.h"
#include <iostream>


TEST(poseType, ThisTestDoesntDoAnything) {
  Pose arbitraryPose;
  arbitraryPose.point = {0.,0.,0.};
  arbitraryPose.orientation = {0.,0.,0.,1.};
}

int main(int argc, char **argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
