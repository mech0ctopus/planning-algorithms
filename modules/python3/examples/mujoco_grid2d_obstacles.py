import os
import random
import time
from typing import Iterable, List, Sequence, Set, Tuple

import mujoco as mj
from mujoco import viewer

from planning.problems.grid2d_problem import (
    build_state_space,
    build_goal_space,
    Grid2dSearchProblem,
    XMAX,
    YMAX,
)
from planning.search.forward import BreadthFirstForwardSearchAlgorithm
from planning.space.primitives import DiscreteStateSpace, DiscreteState
from planning.search.abstract import StateTransitionFunction


# Utilities

def grid_to_world_xy(idx: Tuple[int, int], scale: float = 0.6) -> Tuple[float, float]:
    cx = (XMAX - 1) / 2.0
    cy = (YMAX - 1) / 2.0
    return (idx[0] - cx) * scale, (idx[1] - cy) * scale


# Problem with obstacles

class Grid2dSearchProblemWithObstacles(Grid2dSearchProblem):
    def __init__(self, *, state_space: DiscreteStateSpace, goal_space: DiscreteStateSpace,
                 transition_function: StateTransitionFunction, initial_state: DiscreteState,
                 obstacles: Set[Tuple[int, int]]):
        super().__init__(state_space=state_space, goal_space=goal_space,
                         transition_function=transition_function, initial_state=initial_state)
        self.obstacles = set(obstacles)

    def _is_blocked(self, next_idx: Tuple[int, int]) -> bool:
        return next_idx in self.obstacles

    def get_actions(self, state: DiscreteState):
        actions = super().get_actions(state)
        pruned = []
        x, y = state.index
        for a in actions:
            nidx = (x + a.x, y + a.y)
            if not self._is_blocked(nidx):
                pruned.append(a)
        return pruned

    def get_previous_actions(self, state: DiscreteState):
        actions = super().get_previous_actions(state)
        pruned = []
        x, y = state.index
        for a in actions:
            pidx = (x - a.x, y - a.y)
            if not self._is_blocked(pidx):
                pruned.append(a)
        return pruned


# Obstacle generators

def pattern_wall_with_gap(gap_y: int = None) -> Set[Tuple[int, int]]:
    gap_y = gap_y if gap_y is not None else random.randint(2, YMAX - 3)
    wall_x = XMAX // 2
    obstacles: Set[Tuple[int, int]] = set()
    for y in range(1, YMAX - 1):
        if y != gap_y:
            obstacles.add((wall_x, y))
    return obstacles


def pattern_random_blocks(density: float = 0.18,
                          forbidden: Sequence[Tuple[int, int]] = ()) -> Set[Tuple[int, int]]:
    obstacles: Set[Tuple[int, int]] = set()
    for x in range(1, XMAX - 1):
        for y in range(1, YMAX - 1):
            if random.random() < density:
                obstacles.add((x, y))
    for f in forbidden:
        obstacles.discard(f)
    return obstacles


def pattern_maze(seed: int = None) -> Set[Tuple[int, int]]:
    # Simple randomized DFS maze on odd coordinates
    rng = random.Random(seed)

    def odd(v, vmin, vmax):
        v = max(vmin + 1, min(vmax - 2, v))
        if v % 2 == 0:
            v += 1 if v + 1 < vmax - 1 else -1
        return v

    W, H = XMAX, YMAX
    grid_open: Set[Tuple[int, int]] = set()

    # Initialize: mark all odd cells closed; we'll carve them open
    def neighbors(cx: int, cy: int) -> List[Tuple[int, int, int, int]]:
        res = []
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            wx, wy = cx + dx // 2, cy + dy // 2  # wall between
            if 1 <= nx < W - 1 and 1 <= ny < H - 1:
                res.append((nx, ny, wx, wy))
        rng.shuffle(res)
        return res

    start = (odd(W // 3, 0, W), odd(H // 3, 0, H))
    stack = [start]
    visited = {start}
    grid_open.add(start)

    while stack:
        cx, cy = stack[-1]
        moved = False
        for nx, ny, wx, wy in neighbors(cx, cy):
            if (nx, ny) not in visited:
                # Open wall and next cell
                grid_open.add((wx, wy))
                grid_open.add((nx, ny))
                visited.add((nx, ny))
                stack.append((nx, ny))
                moved = True
                break
        if not moved:
            stack.pop()

    # Obstacles are complement of open cells inside borders
    obstacles: Set[Tuple[int, int]] = set()
    for x in range(1, W - 1):
        for y in range(1, H - 1):
            if (x, y) not in grid_open:
                obstacles.add((x, y))
    return obstacles


def build_problem_with_obstacles(initial_state_index: Tuple[int, int],
                                 goal_state_index: Tuple[int, int],
                                 obstacles: Set[Tuple[int, int]]):
    state_space = build_state_space()
    from planning.problems.grid2d_problem import GridStateTransitionFunction
    problem = Grid2dSearchProblemWithObstacles(
        state_space=state_space,
        goal_space=build_goal_space(goal_state_index),
        transition_function=GridStateTransitionFunction(),
        initial_state=state_space.space[initial_state_index],
        obstacles=obstacles,
    )
    return state_space, problem


# Mujoco XML builder with obstacles visualized as boxes and path overlays

def build_xml(initial_xy: Tuple[float, float], goal_xy: Tuple[float, float],
              obstacle_cells: Set[Tuple[int, int]], plan: List[Tuple[int, int]],
              scale: float = 0.6) -> str:
    obstacle_geoms = []
    half = 0.25 * scale  # half-size in x/y
    height = 0.15
    for (gx, gy) in sorted(obstacle_cells):
        x, y = grid_to_world_xy((gx, gy), scale)
        obstacle_geoms.append(
            f'<geom type="box" pos="{x} {y} {height}" size="{half} {half} {height}" rgba="0.2 0.2 0.8 1" />'
        )
    obstacles_xml = "\n      ".join(obstacle_geoms)

    # Path markers: spheres at nodes and capsules between nodes using fromto
    node_geoms: List[str] = []
    seg_geoms: List[str] = []
    node_r = 0.08
    seg_r = 0.05
    zpath = 0.12
    for i, idx in enumerate(plan):
        x, y = grid_to_world_xy(idx, scale)
        node_geoms.append(
            f'<geom type="sphere" size="{node_r}" pos="{x} {y} {zpath}" rgba="0.1 0.8 0.9 1" />'
        )
        if i > 0:
            x0, y0 = grid_to_world_xy(plan[i - 1], scale)
            seg_geoms.append(
                f'<geom type="capsule" fromto="{x0} {y0} {zpath} {x} {y} {zpath}" size="{seg_r}" rgba="0.1 0.6 0.8 1" />'
            )
    nodes_xml = "\n      ".join(node_geoms)
    segs_xml = "\n      ".join(seg_geoms)

    return f"""
<mujoco model="grid2d_obstacles">
  <compiler angle="degree" coordinate="local"/>
  <option timestep="0.01" gravity="0 0 0"/>
  <asset>
    <texture name="grid" type="2d" builtin="checker" rgb1="0.2 0.2 0.2" rgb2="0.3 0.3 0.3" width="1024" height="1024"/>
    <material name="grid" texture="grid" texrepeat="30 30" texuniform="true" rgba="1 1 1 1"/>
  </asset>
  <worldbody>
    <geom name="floor" type="plane" size="50 50 1" material="grid"/>
    <body name="robot" pos="{initial_xy[0]} {initial_xy[1]} 0.15">
      <freejoint name="root"/>
      <geom type="sphere" size="0.12" rgba="0.1 0.9 0.1 1"/>
    </body>
    <body name="goal" pos="{goal_xy[0]} {goal_xy[1]} 0.15">
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


def simulate_plan(plan_grid: List[Tuple[int, int]], obstacles: Set[Tuple[int, int]],
                  realtime: bool = True) -> None:
    scale = 0.6
    zs = 0.15

    initial_xy = grid_to_world_xy(plan_grid[0], scale)
    goal_xy = grid_to_world_xy(plan_grid[-1], scale)

    xml = build_xml(initial_xy, goal_xy, obstacles, plan_grid, scale)
    model = mj.MjModel.from_xml_string(xml)
    data = mj.MjData(model)

    # Initialize robot orientation as identity quaternion
    data.qpos[0:3] = [initial_xy[0], initial_xy[1], zs]
    data.qpos[3:7] = [1.0, 0.0, 0.0, 0.0]
    mj.mj_forward(model, data)

    headless = os.environ.get("HEADLESS", "0") == "1"

    if headless:
        renderer = mj.Renderer(model, 640, 480)
        outdir = os.environ.get("FRAMES_OUT", "/workspace/frames")
        os.makedirs(outdir, exist_ok=True)
        frame = 0
        for k in range(1, len(plan_grid)):
            x0, y0 = grid_to_world_xy(plan_grid[k - 1], scale)
            x1, y1 = grid_to_world_xy(plan_grid[k], scale)
            steps = 40
            for i in range(steps):
                a = (i + 1) / steps
                x = (1 - a) * x0 + a * x1
                y = (1 - a) * y0 + a * y1
                data.qpos[0:3] = [x, y, zs]
                mj.mj_step(model, data)
                renderer.update_scene(data)
                img = renderer.render()
                from PIL import Image
                Image.fromarray(img).save(os.path.join(outdir, f"frame_{frame:05d}.png"))
                frame += 1
        print(f"Saved {frame} frames to {outdir}.")
        return

    # Interactive viewer with top-down orthographic (if available)
    with viewer.launch_passive(model, data) as v:
        v.cam.lookat[:] = [0.0, 0.0, 0.0]
        v.cam.distance = 8.0
        v.cam.elevation = -90  # top-down
        v.cam.azimuth = 0
        try:
            setattr(v.cam, "orthographic", True)
        except Exception:
            pass

        for k in range(1, len(plan_grid)):
            x0, y0 = grid_to_world_xy(plan_grid[k - 1], scale)
            x1, y1 = grid_to_world_xy(plan_grid[k], scale)
            steps = 40
            for i in range(steps):
                if not v.is_running():
                    return
                a = (i + 1) / steps
                x = (1 - a) * x0 + a * x1
                y = (1 - a) * y0 + a * y1
                data.qpos[0:3] = [x, y, zs]
                mj.mj_step(model, data)
                v.sync()
                if realtime:
                    time.sleep(model.opt.timestep)


if __name__ == "__main__":
    # Choose obstacle pattern via env PATTERN: wall, random, maze
    initial_state_index = (2, 2)
    goal_state_index = (12, 10)

    pattern = os.environ.get("PATTERN", "wall").lower()
    random.seed(int(os.environ.get("SEED", "0")) or None)

    if pattern == "wall":
        obstacles = pattern_wall_with_gap()
    elif pattern == "random":
        obstacles = pattern_random_blocks(0.18, forbidden=[initial_state_index, goal_state_index])
    elif pattern == "maze":
        obstacles = pattern_maze()
        # Ensure start/goal are open
        obstacles.discard(initial_state_index)
        obstacles.discard(goal_state_index)
    else:
        raise SystemExit(f"Unknown PATTERN={pattern}. Use wall|random|maze")

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
