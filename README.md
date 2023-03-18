# planning-algorithms
Experimental implementations of Planning Algorithms by Steven LaValle.

### Installation
```bash
git clone git@github.com:mech0ctopus/planning-algorithms.git
cd planning-algorithms
# Install in editable mode
pip3 install -e .
```

### Tests
```bash
cd planning-algorithms
nosetests3 .
```

### Examples
```bash
cd planning-algorithms/examples
python grid2d.py
python grid3d.py
```

### TODO
- Forward and Backward search should:
    - Either implement an interface
    - OR be passed in as args to a factory
- Integrate "Cost" calculations.

### TODO Later
- Add plot results to problem class
- Implement:
    - Dijkstra's
    - A-Star
    - IterativeDeepening