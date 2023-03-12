"""
This is a module that contains the SuperNode class.
"""
from typing import Any, Callable, Union, Hashable
import yaml
import pandas as pd
from supernodes.operations import InEquality
from copy import copy


yaml.Dumper.ignore_aliases = lambda *args : True


class SuperNode:
    """A node used to create a tree data structure.

    Attributes
    ----------

    name: str, int, hashable, default = None
        The name of the node.

    value: Any, default = None
        The data stored in a node.

    id: Any, default = None
        An attribute that should be unique for every node. None of the nodes in the whole
        tree should to have the same id attribute.

    other_attrs: dict
        Here you can store additional attributes.

    children: list
        A list of children nodes.

    function: Callable, str
        A function to be called when running the tree as a decision tree. This attribute can
        also an inequality as a string. For example: "x >= 10" or "x[1] < 9". Slicing is currently
        not supported.

    child_name_if_true: str, int, hashable
        If this node was run in a binary tree, this attribute will determine which child
        to be chosen next. If the return value of the `function` is ``True``, the child
        with the `name` that is same as `child_name_if_true` will be chosen.
        See :py:meth:`~SuperNode.run_as_binary_tree` for more information.

    child_name_if_false: str, int, hashable
        Specified the child to be chosen if `function` returns ``False``.
        See :py:meth:`~SuperNode.run_as_binary_tree` for more information.

    Examples
    --------

    Importing this class:

    >>> from supernodes import SuperNode

    Making a simple node:

    >>> node = SuperNode()

    Making a node with name, value, and id:

    >>> node = SuperNode(name="main node", value=30, id="node-0")
    >>> node
    (name=main node, value: int, id=node-0)

    Changing the name of the node:

    >>> node.name = "new name"

    Adding children:

    >>> child_1 = SuperNode(name="child-1")
    >>> child_2 = SuperNode(name="child-2")
    >>> node.append(child_1)
    >>> node.append(child_2)
    >>> node
    (name=new name, value: int, id=node-0)
    |__ (name=child-1)
    |__ (name=child-2)

    """

    def __init__(self, name: Union[str, int, Hashable] = None, value: Any = None, id: Any = None,
                 children: list = None, function: Callable = None,
                 child_name_if_true: Union[str, int, Hashable] = None,
                 child_name_if_false: Union[str, int, Hashable] = None, **other_attrs):
        self.name = name
        self.value = value
        self.id = id
        if children:
            self.children = children
        else:
            self.children = []
        self.function = function
        self.child_name_if_true = child_name_if_true
        self.child_name_if_false = child_name_if_false
        self.other_attrs = other_attrs

    def _object_to_node(self, object):
        if type(object) is SuperNode:
            return object
        else:
            node = SuperNode(value=object)
            return node

    def has_children(self):
        """
        Checks if the node has children.

        Returns
        -------
        bool

        """
        return len(self.children) > 0

    def get_children_names(self):
        """
        Lists the names of all children nodes that are directly under this node.

        Returns
        -------
        children: list of str, int, or hashable

        """
        return [child.name for child in self.children if not child.name is None]

    def get_child_from_name(self, name: Union[str, int, Hashable]) -> Union['SuperNode', None]:
        """
        Gets the child node from its name.

        Parameters
        ----------
        name: str, int, hashable

        Returns
        -------
        child: SuperNode
            If a child node having the specified name was found.

        None
            If the child node was not found.

        """
        for child in self.children:
            if child.name == name:
                return child

    def append(self, node: Union['SuperNode', Any]):
        """
        Adds a child node.

        Parameters
        ----------
        node: SuperNode or any object
            If the `node` parameter is not a `SuperNode` object, it will create a new `SuperNode` object.
            The value of the `SuperNode` object will be the value of the `node` parameter.

        """
        node = self._object_to_node(node)
        if node.name in self.get_children_names():
            raise ValueError("Two children of the same Node cannot have the same 'name' attribute.")
        self.children.append(node)

    def insert(self, index, node):
        """
        Adds a child before the specified index in the `children` list.

        Parameters
        ----------
        index: int

        node: SuperNode or any object
            If the `node` parameter is not a `SuperNode` object, it will create a new `SuperNode` object.
            The value of the `SuperNode` object will be the value of the `node` parameter.

        """
        node = self._object_to_node(node)
        if node.name in self.get_children_names():
            raise ValueError("Two children of the same Node cannot have the same 'name' attribute.")
        self.insert(index, node)

    def get_attributes(self, none_attrs=True):
        attrs ={k:v for k, v in self.__dict__.items() if not k.startswith('_') and not k == "other_attrs"}
        for k, v in self.other_attrs:
            attrs[k] = v
        if not none_attrs:
            attrs = {k:v for k,v in attrs.items() if v is not None}
        return attrs

    def __iadd__(self, node):
        self.append(node)
        return self

    def __copy__(self):
        node = SuperNode()
        node.from_node_dict(self.to_node_dict())
        return node

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def _short(self, text):
        text = str(text)
        if len(text) <= 20 and not "\n" in text:
            return text
        new_text = ""
        text = text.strip()
        for char_num in range(20):
            char = text[char_num]
            if char == "\n":
                break
            new_text += char
        new_text += " ..."
        return new_text

    def to_str(self):
        """
        Converts the node and its descendants to a string.

        Returns
        -------
        str

        """
        as_string = "("
        for attr_name, attr in self.get_attributes(none_attrs=False).items():
            if attr_name == "children":
                continue
            elif attr_name == "value":
                as_string += f"{attr_name}: {attr.__class__.__name__}, "
            else:
                as_string += f"{attr_name}={self._short(attr)}, "
        if as_string.endswith(", "):
            as_string = as_string.removesuffix(", ")
        as_string += ")"
        spaces = f"{' ' * 4}"
        for num, child in enumerate(self.children):
            as_string += '\n'
            child_str = child.to_str()
            as_string += f"|"
            as_string += "__ "
            as_string += child_str.splitlines()[0]
            for line in child_str.splitlines()[1:]:
                if num < len(self.children) - 1:
                    as_string += "\n" + "|" + spaces + line
                else:
                    as_string += "\n" + " " + spaces + line
        return as_string

    def to_node_dict(self):
        """
        Converts the node and its descendants to a dictionary.

        Returns
        -------
        dict

        """
        dictionary = {key:value for key, value in self.__dict__.items() if not key.startswith("_") and not key == "children"}
        dictionary["children"] = [child.to_node_dict() for child in self.children]
        return dictionary

    def from_node_dict(self, dictionary):
        """
        Creates a node from a dictionary. The dictionary should have keys that are the same
        as the attributes of the `SuperNode` object (i.e. `name`, `value`, `id`, etc.).

        Parameters
        ----------
        dictionary: dict

        """
        for key, value in dictionary.items():
            if not key == "children":
                if not key in self.__dict__.keys():
                    raise KeyError(f"'{key}' is not an attribute of `Node` object.")
                self.__dict__[key] = value
        self.children = [SuperNode().from_node_dict(child) for child in dictionary['children']]

    def to_yaml(self, file_path):
        """
        Converts the node to a YAML file.

        Parameters
        ----------
        file_path: str
            Path to the YAML file.

        """
        with open(file_path, "w") as file:
            yaml.dump(self.to_node_dict(), file, sort_keys=False)

    def from_yaml(self, file_path):
        """
        Creates a node from a YAML file. The YAML file should have keys that are the same
        as the attributes of the `SuperNode` object (i.e. `name`, `value`, `id`, etc.).

        Parameters
        ----------
        file_path: str
            Path to the YAML file.

        """
        with open(file_path, "rt") as file:
            dictionary = yaml.safe_load(file)
            self.from_node_dict(dictionary)

    def split(self, num: int=2, names: list=None, values: list=None, ids: list=None, functions: list=None,
              **other_attrs_lists):
        """
        Splits the node into children. The number of children created from the node is specified
        by the `num` parameter.

        Parameters
        ----------
        num: int, default = 2
            The number of children to be created.

        names: list (optional)
            If used, the `name` attributes of the children will be the values of the `names` list.
            Its length should be the same as the parameter `num`.

        values: list (optional)
            If used, the `value` attributes of the children will be the values of the `values` list.
            Its length should be the same as the parameter `num`.

        ids: list (optional)
            If used, the `id` attributes of the children will be the values of the `ids` list.
            Its length should be the same as the parameter `num`.

        functions: list (optional)
            If used, the `function` attributes of the children will be the values of the `functions` list.
            Its length should be the same as the parameter `num`.

        other_attrs_list: list (optional)
            If used, the `other_attrs` attributes of the children will be the values of the `other_attrs_lists`.
            Each list length should be the same as the parameter `num`.

        Returns
        -------
        new_children: list of nodes

        """
        new_children = []
        attrs = {"names": [None for _ in range(num)],
                 "values": [None for _ in range(num)],
                 "ids": [None for _ in range(num)],
                 "functions": [None for _ in range(num)],
                 "other_attrs_lists": [{} for _ in range(num)]}
        for attr in [names, values, ids, functions, other_attrs_lists]:
            if attr:
                if len(attr) != num:
                    raise ValueError(f"Length of `{attr.__name__}` should be same as `num`.")
                attrs[attr.__name__] = attr
        for i in range(num):
            node = SuperNode(name=attrs['names'][i],
                            value=attrs['values'][i],
                            id=attrs['ids'][i],
                            function=attrs['functions'][i],
                            **attrs['other_attrs_lists'][i])
            new_children.append(node)
        self.children += new_children
        return new_children

    def to_list(self, attr=None):
        """
        This method will convert the tree to a list of nodes names. Each row in the list is a path from the
        current node to a leaf.

        Returns
        -------
        arr: list
            List of rows. Each row consists of nodes names.

        """
        arr = []
        row = []
        for row in self._rows_iter(row, attr):
            arr.append(row)
        return arr

    def split_on_df_column(self, df, column):
        """
        Splits the node based on the columns of a `pandas` `DataFrame`. The number of children nodes
        will depend on the number of unique values in the column. Each unique value will be the `name`
        attribute of a child node.

        Parameters
        ----------
        df: pandas.DataFrame

        column
            One of the columns of the `DataFrame`.

        Returns
        -------
        nodes: list of children nodes

        Examples
        --------

        >>> import pandas as pd
        >>> df = pd.DataFrame({"Column-1": ["column-1 row-1", "column-1 row-2"],
        ...                    "Column-2": ["column-2 row-1", "column-2 row-2"]})
        >>> node = SuperNode("DataFrame Node")
        >>> node.split_on_df_column(df, "Column-1")
        [(name=column-1 row-1, value: DataFrame), (name=column-1 row-2, value: DataFrame)]
        >>> node
        (name=DataFrame Node)
        |__ (name=column-1 row-1, value: DataFrame)
        |__ (name=column-1 row-2, value: DataFrame)

        """
        nodes = []
        unique_values = df[column].unique()
        for unique_value in unique_values:
            node = SuperNode(name=unique_value, value=df[df[column] == unique_value])
            nodes.append(node)
            self.append(node)
        return nodes

    def from_df(self, df):
        """
        Creates a tree from a `pandas` `DataFrame`. It will apply the method: :py:meth:`~SuperNode.split_on_df_column`.
        to each column in the `DataFrame`.

        Parameters
        ----------
        df: pandas.DataFrame

        Examples
        --------

        >>> import pandas as pd
        >>> df = pd.DataFrame({"Column-1": ["column-1 row-1", "column-1 row-2"],
        ...                    "Column-2": ["column-2 row-1", "column-2 row-2"]})
        >>> node = SuperNode("DataFrame Node")
        >>> node.from_df(df)
        >>> node
        (name=DataFrame Node)
        |__ (name=column-1 row-1, value: DataFrame)
        |    |__ (name=column-2 row-1, value: DataFrame)
        |__ (name=column-1 row-2, value: DataFrame)
             |__ (name=column-2 row-2, value: DataFrame)

        """
        if len(df.columns) > 0:
            nodes = self.split_on_df_column(df, column=df.columns[0])
            for node in nodes:
                smaller_df = node.value[df.columns[1:]]
                node.from_df(smaller_df)

    def _rows_iter(self, row, attr):
        row = copy(row)
        if not attr:
            row.append(self)
        else:
            if attr in [key for key in self.__dict__.keys() if not key.startswith("_")]:
                row.append(self.__dict__[attr])
            elif attr in self.other_attrs.keys():
                row.append(self.other_attrs[attr])
        if not self.has_children():
            yield row
        for child in self.children:
            for new_row in child._rows_iter(row=row, attr=attr):
                yield new_row

    def to_df(self, columns=None, ignore_first=True, attr="name"):
        """
        Creates a `pandas` `DataFrame` from the tree. Each layer beneath this node will become a column.
        The values under the columns are the `name` attributes of the nodes in the tree.

        Parameters
        ----------
        columns: list, default = None
            The column headers for the `DataFrame`.

        ignore_first: bool, default=True
            If ``True``, the current node will not be included in the `DataFrame`.

        Returns
        -------
        df: pandas.DataFrame

        """
        if ignore_first:
            data = [l[1:] for l in self.to_list(attr=attr)]
        else:
            data = self.to_list(attr=attr)
        df = pd.DataFrame(data, columns=columns)
        return df

    def find_node(self, id):
        """
        Returns a descendant node that has the specified `id` attribute.

        Parameters
        ----------
        id: Any
            The `id` attribute of the node.

        Returns
        -------
        child: SuperNode

        None

        """
        for child in self.children:
            if child.id == id:
                return child
            if child.find_node(id=id):
                return child

    def find_nodes(self, name=None, value=None, function=None, **other_attrs):
        """
        Returns a list of descendant nodes that match the specified criteria.

        Parameters
        ----------
        name: str, int, hashable

        value: Any

        function: Callable, str

        Returns
        -------
        descendants: list of nodes

        """
        descendants = []
        for child in self.children:
            add_child = True
            if name and child.name != name:
                add_child = False
            if value and child.value != value:
                add_child = False
            if function and child.function != function:
                add_child = False
            if other_attrs != {}:
                for key, value in other_attrs.items():
                    if not key in child.other_attrs.keys():
                        add_child = False
                    elif value != child.other_attrs[key]:
                        add_child = False
            if add_child:
                descendants.append(child)
            descendants += child.find_nodes(name=name, value=value, function=function, **other_attrs)
        return descendants

    def __getitem__(self, name):
        """
        Gets a child from its name.

        Parameters
        ----------
        name: str, int, hashable

        Returns
        -------
        node

        """
        return self.get_child_from_name(name)

    def __setitem__(self, name, node):
        """
        Adds a new child and giving it the specified `name`.

        Parameters
        ----------
        name: str, int, hashable

        node: SuperNode, Any

        """
        for i, child in enumerate(self.children):
            if child.name == name:
                self.children.pop(i)
                break
        node = self._object_to_node(node)
        node.name = name
        self.append(node)

    def run_as_binary_tree(self, **kwargs):
        """
        Runs the tree as a binary decision tree. It will run the `function` attribute of this node,
        then chooses a child node and runs its `function`, then chooses one of the child's
        children, etc. It chooses the children based on the attributes `child_name_if_true` and
        `child_name_if_false`. If the output of `function` is ``True``, the next child will be
        the node whose `name` is same as `child_name_if_true`. If the output of `function` is ``False``,
        the next child will be the node whose `name` is same as `child_name_if_false`.

        Creating a tree that can be used as a binary decision tree:

        >>> main_node = SuperNode(name="main-node", function="x > 10")
        >>> main_node['first-child'] = SuperNode()
        >>> main_node['second-child'] = SuperNode()
        >>> main_node.child_name_if_true = "first-child"
        >>> main_node.child_name_if_false = "second-child"

        Running the binary decision tree:

        >>> leaf = main_node.run_as_binary_tree(x=11)
        >>> leaf
        (name=first-child)

        Parameters
        ----------
        kwargs
            Keyword arguments that the functions inside the tree accepts.

        Returns
        -------
        node: SuperNode
            Either the leaf node will be returned or a node that has no function.

        """
        if not self.function:
            return self
        if type(self.function) is str:
            output = InEquality(self.function)(**kwargs)
        else:
            output = self.function(**kwargs)
        if output:
            if self.child_name_if_true:
                child = self.get_child_from_name(self.child_name_if_true)
                if child:
                    return child.run_as_binary_tree(**kwargs)
        elif output is False:
            if self.child_name_if_false:
                child = self.get_child_from_name(self.child_name_if_false)
                if child:
                    return child.run_as_binary_tree(**kwargs)
        return self

if __name__ == "__main__":
    import doctest
    doctest.testmod()