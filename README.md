# planning-algorithms
Experimental implementations of Planning Algorithms by Steven LaValle.

### Installation
```bash
git clone git@github.com:mech0ctopus/planning-algorithms.git

## C++
cd planning-algorithms/modules/cpp
mkdir build && cd build
cmake ..
make

## Python
cd planning-algorithms/modules/python3
# Install in editable mode (don't forget the period at the end)
pip3 install -e .
```

### Tests
```bash
## Run all tests
cd planning-algorithms
./run_tests.sh

## C++
cd planning-algorithms/modules/cpp/build
./TestPrimitives

## Python
cd planning-algorithms/modules/python3
nosetests3 .
```

### Examples
```bash
cd planning-algorithms/modules/python3/examples
python grid2d.py
python grid3d.py
python five_state.py
```

### TODO
- `FiveState`
  - Understand why state is replicated in bi-directional plan


### TODO Later
- Add assertions about the plan that is created.
- Mark Initial/Goal States as VISITED in bidirectional search
- Define a better `SearchProblem` interface
- Begin optimal planning work
  - Integrate "Cost" calculations.
  - Create Python version of 5-state optimal planning problem 

### Maybe Later
- Create/Implement more examples
- Determine a path forward for C++ work
- Identify a better design pattern to use for constructing Forward/Backward versions
  of the same search algo. (Factory?)
    - Should Forward, Backward, and Bidirectional search be consolidated into a Unified interface?
- Implement:
    - Dijkstra's
    - A-Star
    - IterativeDeepening
- Add plot results to problem class
- Raise exception if search fails (instead of Return code)
- Add logic to `ForwardSearch` for checking if a state is `alive` or `dead` per p.33
