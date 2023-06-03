# Overview
SuperNodes is a Python package that creates tree data structures easily.
It is designed to be similar to Python dictionaries but with more
functions. The trees can be used:
* For storing data
* As decision trees
* Both for storing data and as decision trees.

# How to install
Run this command to install SuperNodes:
```shell
pip install supernodes
```

# How to create a tree
To create a tree, first create the root node:

```python
from supernodes import SuperNode

root_node = SuperNode(name="root")
```

You can add children nodes to the root node using different methods:

* Using ``append`` function:
```python
child_1 = SuperNode(name="child-1")
child_2 = SuperNode(name="child-2")
root_node.append(child_1)
root_node.append(child_2)
```
* Using indexer:
```python
root_node['child-1'] = SuperNode()
root_node['child-2'] = SuperNode()
```
* Using `split`:
```python
root_node.split(num=2, names=['child-1', 'child-2'])
```
You can view more methods for adding children nodes
[SuperNodes methods](https://supernodes.herokuapp.com/Examples.methods.html).

# How to use as a decision tree
To create a tree that can be used as a decision tree,
create the root node and add an inequality string or
a function inside the `function` parameter:
```python
root_node = SuperNode(name="root-node", function="x > 10")
```
Then create the children and add their names to the attributes,
`child_name_if_true` and `child_name_if_false`.
```python
root_node['first-child'] = SuperNode()
root_node['second-child'] = SuperNode()
root_node.child_name_if_true = "first-child"
root_node.child_name_if_false = "second-child"
```
Run the decision tree:
```python
leaf = root_node.run_as_binary_tree(x=11)
```
# Extra
# Documentation
You can find the documentation in this link:
[SuperNodes docs](https://supernodes.herokuapp.com/).

# More examples
You can find more examples this link:
[SuperNodes examples](https://supernodes.herokuapp.com/Examples.html).

# License and Copyrights
Copyrights (c) 2023 Mubarak Almehairbi.
This package is licensed under the MIT license.
