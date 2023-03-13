"""
Different ways of creating trees

Different ways of creating trees using SuperNodes are presented below.
"""
import pandas as pd
from supernodes import SuperNode

# Method 1: using `append`
root = SuperNode(name="root", value=0)
child_1 = SuperNode(name="child-1")
child_2 = SuperNode(name="child-2")
root.append(child_1)
root.append(child_2)

# Method 2: using += operator
root = SuperNode(name="root", value=0)
child_1 = SuperNode(name="child-1")
child_2 = SuperNode(name="child-2")
root += child_1
root += child_2

# Method 3: using `insert`
root = SuperNode(name="root", value=0)
child_1 = SuperNode(name="child-1")
child_2 = SuperNode(name="child-2")
root.insert(0, child_1)
root.insert(1, child_2)

# Method 4: using indexer
root = SuperNode(name="root", value=0)
root["child-1"] = SuperNode()
root["child-2"] = SuperNode()

# Method 5: using `split`
root = SuperNode(name="root", value=0)
root.split(num=2, names=["child-1", "child-2"])

# Method 6: from pandas DataFrame column
df = pd.DataFrame({"children": ["child-1", "child-2"]})
root = SuperNode(name="root", value=0)
root.split_on_df_column(df, column="children")
