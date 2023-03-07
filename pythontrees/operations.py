import operator
from decimal import Decimal


operators = {"<": operator.lt,
          "<=": operator.le,
          "==": operator.eq,
          "!=": operator.ne,
          ">=": operator.ge,
          ">": operator.gt,}

def _is_int(string_num):
    return string_num.isdigit()


def _is_decimal(string_num):
    if _is_int(string_num): return False
    try:
        float(string_num)
        return True
    except ValueError:
        return False


class InEquality:
    """
    Runs an inequality operation from an inequality string.
    This is helpful when running a tree as a decision tree.

    Examples
    --------

    Running an inequality:

    >>> inequality = InEquality("x == 10")
    >>> inequality(x=7)
    False

    >>> inequality = InEquality("x == -10")
    >>> inequality(x=-10)
    True

    >>> inequality = InEquality("y != 9.01")
    >>> inequality(y=9.01)
    False

    Including an inequality in a binary decision tree:

    >>> from pythontrees import DataNode
    >>> inequality = InEquality("x < 100")
    >>> main_node = DataNode(name="main-node", function=inequality)
    >>> main_node['first-child'] = DataNode()
    >>> main_node['second-child'] = DataNode()
    >>> main_node.child_name_if_true = "first-child"
    >>> main_node.child_name_if_false = "second-child"

    Running the decision tree:

    >>> main_node.run_as_binary_tree(x=101)
    (name=second-child, value: NoneType)

    """
    def __init__(self, inequality: str, strings_to_numbers=True):
        """

        Parameters
        ----------
        inequality: str
            The inequality represented as a string.

        strings_to_numbers: bool
            If ``True``, each string that can be converted to an ``int`` or ``float`` will be converted.

        """
        inequality_list = inequality.split()
        if len(inequality_list) != 3:
            raise ValueError(f"Splitting the inequality resulted in {len(inequality_list)} parts instead of 3 parts.")
        self.left = inequality_list[0]
        self.middle = inequality_list[1]
        self.right = inequality_list[2]
        self.strings_to_numbers = strings_to_numbers

    def __call__(self, **kwargs):
        left = self.left
        right = self.right
        for key, value in kwargs.items():
            if left == key: left = value
            if right == key: right = value
        if self.strings_to_numbers:
            if type(left) is str:
                if _is_int(left):
                    left = int(left)
                elif _is_decimal(left):
                    left = Decimal(left)
            if type(right) is str:
                if _is_int(right):
                    right = int(right)
                elif _is_decimal(right):
                    right = float(right)
        oper = operators[self.middle]
        out = oper(left, right)
        return out




if __name__ == "__main__":
    import doctest
    doctest.testmod()

