import os
import random
import time
from typing import List, Sequence, Set, Tuple

import mujoco as mj
from mujoco import viewer

from planning.problems.grid3d_problem import (
    build_state_space,
    build_goal_space,
    Grid3dSearchProblem,
    XMAX,
    YMAX,
    ZMAX,
)
from planning.search.forward import BreadthFirstForwardSearchAlgorithm
from planning.space.primitives import DiscreteStateSpace, DiscreteState
from planning.search.abstract import StateTransitionFunction


# Utilities

def grid_to_world_xyz(idx: Tuple[int, int, int], scale: float = 0.5) -> Tuple[float, float, float]:
    cx = (XMAX - 1) / 2.0
    cy = (YMAX - 1) / 2.0
    cz = (ZMAX - 1) / 2.0
    return (idx[0] - cx) * scale, (idx[1] - cy) * scale, (idx[2] - cz) * scale + 0.15


# Problem with obstacles (3D)

class Grid3dSearchProblemWithObstacles(Grid3dSearchProblem):
    def __init__(self, *, state_space: DiscreteStateSpace, goal_space: DiscreteStateSpace,
                 transition_function: StateTransitionFunction, initial_state: DiscreteState,
                 obstacles: Set[Tuple[int, int, int]]):
        super().__init__(state_space=state_space, goal_space=goal_space,
                         transition_function=transition_function, initial_state=initial_state)
        self.obstacles = set(obstacles)

    def _is_blocked(self, next_idx: Tuple[int, int, int]) -> bool:
        return next_idx in self.obstacles

    def get_actions(self, state: DiscreteState):
        actions = super().get_actions(state)
        pruned = []
        x, y, z = state.index
        for a in actions:
            nidx = (x + a.x, y + a.y, z + a.z)
            if not self._is_blocked(nidx):
                pruned.append(a)
        return pruned

    def get_previous_actions(self, state: DiscreteState):
        actions = super().get_previous_actions(state)
        pruned = []
        x, y, z = state.index
        for a in actions:
            pidx = (x - a.x, y - a.y, z - a.z)
            if not self._is_blocked(pidx):
                pruned.append(a)
        return pruned


# Obstacle patterns (3D)

def pattern_wall_with_gap_3d(axis: str = "x", gap_coord: Tuple[int, int] = None) -> Set[Tuple[int, int, int]]:
    obstacles: Set[Tuple[int, int, int]] = set()
    if axis == "x":
        wx = XMAX // 2
        gy = (YMAX // 2) if gap_coord is None else gap_coord[0]
        gz = (ZMAX // 2) if gap_coord is None else gap_coord[1]
        for y in range(1, YMAX - 1):
            for z in range(1, ZMAX - 1):
                if not (abs(y - gy) <= 1 and abs(z - gz) <= 1):
                    obstacles.add((wx, y, z))
    elif axis == "y":
        wy = YMAX // 2
        gx = (XMAX // 2) if gap_coord is None else gap_coord[0]
        gz = (ZMAX // 2) if gap_coord is None else gap_coord[1]
        for x in range(1, XMAX - 1):
            for z in range(1, ZMAX - 1):
                if not (abs(x - gx) <= 1 and abs(z - gz) <= 1):
                    obstacles.add((x, wy, z))
    else:  # axis == "z"
        wz = ZMAX // 2
        gx = (XMAX // 2) if gap_coord is None else gap_coord[0]
        gy = (YMAX // 2) if gap_coord is None else gap_coord[1]
        for x in range(1, XMAX - 1):
            for y in range(1, YMAX - 1):
                if not (abs(x - gx) <= 1 and abs(y - gy) <= 1):
                    obstacles.add((x, y, wz))
    return obstacles


def pattern_random_blocks_3d(density: float = 0.08,
                             forbidden: Sequence[Tuple[int, int, int]] = ()) -> Set[Tuple[int, int, int]]:
    obstacles: Set[Tuple[int, int, int]] = set()
    for x in range(1, XMAX - 1):
        for y in range(1, YMAX - 1):
            for z in range(1, ZMAX - 1):
                if random.random() < density:
                    obstacles.add((x, y, z))
    for f in forbidden:
        obstacles.discard(f)
    return obstacles


def build_problem_with_obstacles(initial_state_index: Tuple[int, int, int],
                                 goal_state_index: Tuple[int, int, int],
                                 obstacles: Set[Tuple[int, int, int]]):
    state_space = build_state_space()
    from planning.problems.grid3d_problem import GridStateTransitionFunction
    problem = Grid3dSearchProblemWithObstacles(
        state_space=state_space,
        goal_space=build_goal_space(goal_state_index),
        transition_function=GridStateTransitionFunction(),
        initial_state=state_space.space[initial_state_index],
        obstacles=obstacles,
    )
    return state_space, problem


# Mujoco XML builder (3D) with obstacles and path overlays

def build_xml(initial_xyz: Tuple[float, float, float], goal_xyz: Tuple[float, float, float],
              obstacle_cells: Set[Tuple[int, int, int]], plan: List[Tuple[int, int, int]],
              scale: float = 0.5) -> str:
    # Obstacles: boxes at each occupied voxel
    obstacle_geoms = []
    hx = 0.22 * scale
    hy = 0.22 * scale
    hz = 0.22 * scale
    for (gx, gy, gz) in sorted(obstacle_cells):
        x, y, z = grid_to_world_xyz((gx, gy, gz), scale)
        obstacle_geoms.append(
            f'<geom type="box" pos="{x} {y} {z}" size="{hx} {hy} {hz}" rgba="0.2 0.2 0.8 1" />'
        )
    obstacles_xml = "\n      ".join(obstacle_geoms)

    # Path: spheres and capsules
    node_geoms: List[str] = []
    seg_geoms: List[str] = []
    node_r = 0.06
    seg_r = 0.045
    for i, idx in enumerate(plan):
        x, y, z = grid_to_world_xyz(idx, scale)
        node_geoms.append(
            f'<geom type="sphere" size="{node_r}" pos="{x} {y} {z}" rgba="0.1 0.8 0.9 1" />'
        )
        if i > 0:
            x0, y0, z0 = grid_to_world_xyz(plan[i - 1], scale)
            seg_geoms.append(
                f'<geom type="capsule" fromto="{x0} {y0} {z0} {x} {y} {z}" size="{seg_r}" rgba="0.1 0.6 0.8 1" />'
            )
    nodes_xml = "\n      ".join(node_geoms)
    segs_xml = "\n      ".join(seg_geoms)

    return f"""
<mujoco model="grid3d_obstacles">
  <compiler angle="degree" coordinate="local"/>
  <option timestep="0.01" gravity="0 0 0"/>
  <asset>
    <texture name="grid" type="2d" builtin="checker" rgb1="0.2 0.2 0.2" rgb2="0.3 0.3 0.3" width="1024" height="1024"/>
    <material name="grid" texture="grid" texrepeat="30 30" texuniform="true" rgba="1 1 1 1"/>
  </asset>
  <worldbody>
    <geom name="floor" type="plane" size="50 50 1" material="grid"/>
    <body name="robot" pos="{initial_xyz[0]} {initial_xyz[1]} {initial_xyz[2]}">
      <freejoint name="root"/>
      <geom type="sphere" size="0.11" rgba="0.1 0.9 0.1 1"/>
    </body>
    <body name="goal" pos="{goal_xyz[0]} {goal_xyz[1]} {goal_xyz[2]}">
      <geom type="sphere" size="0.14" rgba="0.9 0.1 0.1 1"/>
    </body>
    <!-- Obstacles -->
    {obstacles_xml}
    <!-- Path nodes -->
    {nodes_xml}
    <!-- Path segments -->
    {segs_xml}
  </worldbody>
</mujoco>
"""


def simulate_plan(plan_grid: List[Tuple[int, int, int]], obstacles: Set[Tuple[int, int, int]],
                  realtime: bool = True) -> None:
    scale = 0.5

    initial_xyz = grid_to_world_xyz(plan_grid[0], scale)
    goal_xyz = grid_to_world_xyz(plan_grid[-1], scale)

    xml = build_xml(initial_xyz, goal_xyz, obstacles, plan_grid, scale)
    model = mj.MjModel.from_xml_string(xml)
    data = mj.MjData(model)

    # Initialize robot orientation as identity quaternion
    data.qpos[0:3] = [initial_xyz[0], initial_xyz[1], initial_xyz[2]]
    data.qpos[3:7] = [1.0, 0.0, 0.0, 0.0]
    mj.mj_forward(model, data)

    headless = os.environ.get("HEADLESS", "0") == "1"

    if headless:
        renderer = mj.Renderer(model, 640, 480)
        outdir = os.environ.get("FRAMES_OUT", "/workspace/frames")
        os.makedirs(outdir, exist_ok=True)
        frame = 0
        for k in range(1, len(plan_grid)):
            x0, y0, z0 = grid_to_world_xyz(plan_grid[k - 1], scale)
            x1, y1, z1 = grid_to_world_xyz(plan_grid[k], scale)
            steps = 40
            for i in range(steps):
                a = (i + 1) / steps
                x = (1 - a) * x0 + a * x1
                y = (1 - a) * y0 + a * y1
                z = (1 - a) * z0 + a * z1
                data.qpos[0:3] = [x, y, z]
                mj.mj_step(model, data)
                renderer.update_scene(data)
                img = renderer.render()
                from PIL import Image
                Image.fromarray(img).save(os.path.join(outdir, f"frame_{frame:05d}.png"))
                frame += 1
        print(f"Saved {frame} frames to {outdir}.")
        return

    with viewer.launch_passive(model, data) as v:
        v.cam.lookat[:] = [0.0, 0.0, 0.0]
        v.cam.distance = 10.0
        v.cam.elevation = -90  # top-down along +z
        v.cam.azimuth = 0
        try:
            setattr(v.cam, "orthographic", True)
        except Exception:
            pass

        for k in range(1, len(plan_grid)):
            x0, y0, z0 = grid_to_world_xyz(plan_grid[k - 1], scale)
            x1, y1, z1 = grid_to_world_xyz(plan_grid[k], scale)
            steps = 40
            for i in range(steps):
                if not v.is_running():
                    return
                a = (i + 1) / steps
                x = (1 - a) * x0 + a * x1
                y = (1 - a) * y0 + a * y1
                z = (1 - a) * z0 + a * z1
                data.qpos[0:3] = [x, y, z]
                mj.mj_step(model, data)
                v.sync()
                if realtime:
                    time.sleep(model.opt.timestep)


if __name__ == "__main__":
    # Choose obstacle pattern via env PATTERN: wall|random
    initial_state_index = (1, 2, 3)
    goal_state_index = (12, 13, 10)

    pattern = os.environ.get("PATTERN", "wall").lower()
    random.seed(int(os.environ.get("SEED", "0")) or None)

    if pattern == "wall":
        obstacles = pattern_wall_with_gap_3d(axis=os.environ.get("AXIS", "x"))
    elif pattern == "random":
        obstacles = pattern_random_blocks_3d(0.06, forbidden=[initial_state_index, goal_state_index])
    else:
        raise SystemExit(f"Unknown PATTERN={pattern}. Use wall|random")

    state_space, problem = build_problem_with_obstacles(initial_state_index, goal_state_index, obstacles)

    solver = BreadthFirstForwardSearchAlgorithm(problem)
    ok = solver.search()
    print(f"Planning success: {ok}")
    if not ok:
        raise SystemExit(1)

    plan_states = solver.get_plan()
    plan_grid_idx = [s.index for s in plan_states]
    print(f"Plan length: {len(plan_grid_idx)} states; obstacles: {len(obstacles)}; pattern={pattern}")

    simulate_plan(plan_grid_idx, obstacles, realtime=True)
