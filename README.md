# epyjson: e-JSON library for python
Python library for the e-JSON electricity network data format.

## Introduction

e-JSON is a JSON-based format for representing electricity network data. The `epyjson` package wraps e-JSON in a python `EJson` object that allows easy manipulation, for example retrieving network components, adding or removing components, depth first search traversal and so on.

The package consists of two modules: `ejson`, which provides the `EJson` class, and `utils`, which provides additional utilities for various manipulations.

The `EJson` class is based on the [`networkx`](https://networkx.org) package. The methods in `EJson` provide core functionality, and are mostly agnostic of the details of the e-JSON data format.

On the other hand, the `utils` module provides additional non-core functionality, and is often more concerned with details of the data format. 

## Installation
```
pip install .
# or "pip install -e ." for development
```

## Unit tests
```
pytest -s -v
```

## Example
This example is found in `examples/example.py`.

```python3
import epyjson

# Load in the network
netw = epyjson.EJson.read_from_file(
    '../tests/test_networks/netw_generic_a.json'
)

# Directly obtain and manipulate the underlying networkx graph. Normally, we
# would only do this under special circumstances.
nx_nodes = list(netw.graph.subgraph(['nd1', 'nd2']))

# Obtain a list of components of type Line. Note that components(...) returns a generator
# so it is often convenient to wrap it in list(...).
lines = list(netw.components(ctype='Line'))

# Obtain raw e-JSON dict.
raw = netw.raw_ejson()

# Obtain connections from ln2_3 to connected nodes.
line_cons = list(netw.connections_from('ln2_3'))
# Obtain data from first such connection.
ln2_3_id, node_id, con_idx, con_data = line_cons[0]

# Apply network reduction: telescope long strings of lines together, etc.
epyjson.reduce_network(netw)
```
