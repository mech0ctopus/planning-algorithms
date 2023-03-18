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
- Identify a better design pattern to use for constructing Forward/Backward versions
  of the same search algo.
    - Forward and Backward search should:
        - Either implement an interface
        - OR be passed in as args to a factory

### TODO Later
- Integrate "Cost" calculations.
- Add plot results to problem class
- Implement:
    - Dijkstra's
    - A-Star
    - IterativeDeepening
- Raise exception if search fails (instead of Return code)
- Add logic to `ForwardSearch` for checking if a state is `alive` or `dead` per p.33