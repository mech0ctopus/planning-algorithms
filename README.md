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
- Finish implementing bidirectional search
  - Resolve how to produce full plan in `bidirectional.py`
    - Need to calculate/store both the forward half of the plan and the backward half of the plan.
  - There is some issue/inconvenience with the shared "state space" data structure between the two search branches
- Don't skip bidirectional tests

### TODO Later
- Define a better `SearchProblem` interface
- Integrate "Cost" calculations.

### Maybe Later
- Identify a better design pattern to use for constructing Forward/Backward versions
  of the same search algo. (Factory?)
    - Should Forward, Backward, and Bidirectional search be consolidated into a Unified interface?
- Create/Implement more examples
- Implement:
    - Dijkstra's
    - A-Star
    - IterativeDeepening
- Add plot results to problem class
- Raise exception if search fails (instead of Return code)
- Add logic to `ForwardSearch` for checking if a state is `alive` or `dead` per p.33
