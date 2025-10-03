import os
import time
from typing import List, Tuple

import mujoco as mj
from mujoco import viewer

from planning.problems.grid2d_problem import build_problem, XMAX, YMAX
from planning.search.forward import BreadthFirstForwardSearchAlgorithm


def grid_to_world_xy(idx: Tuple[int, int], scale: float = 0.6) -> Tuple[float, float]:
    cx = (XMAX - 1) / 2.0
    cy = (YMAX - 1) / 2.0
    return (idx[0] - cx) * scale, (idx[1] - cy) * scale


def build_xml(initial_xy: Tuple[float, float], goal_xy: Tuple[float, float]) -> str:
    return f"""
<mujoco model="grid2d">
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
  </worldbody>
</mujoco>
"""


def simulate_plan(plan_grid: List[Tuple[int, int]], realtime: bool = True) -> None:
    scale = 0.6
    zs = 0.15

    initial_xy = grid_to_world_xy(plan_grid[0], scale)
    goal_xy = grid_to_world_xy(plan_grid[-1], scale)

    xml = build_xml(initial_xy, goal_xy)
    model = mj.MjModel.from_xml_string(xml)
    data = mj.MjData(model)

    # Initialize robot orientation as identity quaternion
    data.qpos[0:3] = [initial_xy[0], initial_xy[1], zs]
    data.qpos[3:7] = [1.0, 0.0, 0.0, 0.0]
    mj.mj_forward(model, data)

    headless = os.environ.get("HEADLESS", "0") == "1"

    if headless:
        # Offscreen rendering with Renderer, save frames to disk
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
        print(f"Saved {frame} frames to {outdir}. Combine into a video with ffmpeg if desired.")
        return

    # Interactive viewer
    with viewer.launch_passive(model, data) as v:
        v.cam.lookat[:] = [0.0, 0.0, 0.0]
        v.cam.distance = 6.0
        v.cam.elevation = -30
        v.cam.azimuth = 90

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
    # Build a 2D grid problem and solve with Breadth-First Forward Search
    initial_state_index = (2, 2)
    goal_state_index = (12, 10)

    state_space, problem = build_problem(initial_state_index, goal_state_index)
    solver = BreadthFirstForwardSearchAlgorithm(problem)
    ok = solver.search()
    print(f"Planning success: {ok}")
    if not ok:
        raise SystemExit(1)

    plan_states = solver.get_plan()
    plan_grid_idx = [s.index for s in plan_states]
    print(f"Plan length: {len(plan_grid_idx)} states")

    simulate_plan(plan_grid_idx, realtime=True)
