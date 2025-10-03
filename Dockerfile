# syntax=docker/dockerfile:1
# Base image with Python and common build tools
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MUJOCO_GL=egl

# System deps for Python 3.10, Mujoco (GLFW/EGL), and viewer support
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip python3-dev build-essential \
    libgl1 libgl1-mesa-dri libgles2 libegl1 \
    libx11-6 libxext6 libxrandr2 libxinerama1 libxcursor1 libxi6 libxxf86vm1 \
    libglfw3 libxkbcommon0 \
    libosmesa6 \
    git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy repo
WORKDIR /workspace
COPY . /workspace

# Install Python deps
# - Install mujoco (Python bindings)
# - glfw for the interactive viewer
# - Install our planning package in editable mode
RUN pip install --upgrade pip setuptools wheel \
    && pip install "mujoco>=3.1" glfw pillow matplotlib \
    && pip install -e ./modules/python3

# Default command: run the Mujoco planning demo (headless by default via MUJOCO_GL=egl)
CMD ["python", "modules/python3/examples/mujoco_grid2d.py"]
