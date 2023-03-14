import unittest
from supernodes import SuperNode

class TestTree(unittest.TestCase):

    def test_create_children(self):
        root = SuperNode(name="root", value=0)
        root["child-1"] = SuperNode(value=1)
        root["child-2"] = SuperNode(value=2)
        self.assertEqual(len(root.children), 2)

    def test_decision_tree(self):
        root = SuperNode(name="root", function="x[0] > 1")
        root.child_name_if_true = "child-1"
        root.child_name_if_false = "child-2"
        root["child-1"] = SuperNode(value=1, function="x[1] == 0")
        root["child-1"].child_name_if_true = "grandchild-1"
        root["child-1"].child_name_if_false = "grandchild-2"
        root["child-2"] = SuperNode(value=2)
        root['child-1']['grandchild-1'] = SuperNode(value=3)
        root['child-1']['grandchild-2'] = SuperNode(value=4)
        leaf = root.run_as_binary_tree(x=[2, 0])
        self.assertEqual(leaf.value, 3)
        leaf2 = root.run_as_binary_tree(x=[0, 2])
        self.assertEqual(leaf2.value, 2)

if __name__ == "__main__":
    unittest.main()

