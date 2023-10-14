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
python optimal_grid2d.py
python optimal_grid3d.py
python optimal_five_state.py
```

### TODO
- Update unit tests for ForwardLabelCorrecting

### TODO Later
- Optimal Planning with Forward Value Iteration

### Maybe Later
- Implement:
    - A-Star
    - IterativeDeepening
- Define a better `SearchProblem` interface
- Mark Initial/Goal States as VISITED in bidirectional search
- Create/Implement more examples
- Determine a path forward for C++ work
- Identify a better design pattern to use for constructing Forward/Backward versions
  of the same search algo. (Factory?)
    - Should Forward, Backward, and Bidirectional search be consolidated into a Unified interface?
- Add plot results to problem class
- Raise exception if search fails (instead of Return code)
- Add logic to `ForwardSearch` for checking if a state is `alive` or `dead` per p.33
