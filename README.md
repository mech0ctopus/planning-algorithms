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
- Consider moving problems into a `planning/problems` folder so they can be imported.
- Add plot results to problem class