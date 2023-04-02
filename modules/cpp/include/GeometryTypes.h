#pragma once

struct Position{
    double x, y, z;
};

struct Quaternion{
    double x, y, z, w;
};

struct Pose{
    Position point;
    Quaternion orientation;
};

struct Twist2d{
    double vx, wz;
};
