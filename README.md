# planning-algorithms
Experimental implementations of Planning Algorithms by Steven LaValle.

### Installation
```bash
git clone ...
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
python 2d_grid.py
```

### TODO
- Add plot results to problem class
- Integrate "Cost" calculations.
- Tests
    - Resolve why DepthFirst is not working in test
- Forward and Backward search should:
    - Either implement an interface
    - OR be passed in as args to a factory

- Implement:
    - Dijkstra's
    - A-Star
    - IterativeDeepening