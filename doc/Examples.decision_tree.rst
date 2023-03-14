Creating decision tree
======================

Below is an example on how to create and run a decision tree.

.. code-block:: python

   
   x1 = [10, 12, 40]
   x2 = [11, 6, 5]
   
   root = SuperNode(name="root", function="x[0] < 11", child_name_if_true="true-child", child_name_if_false="false-child")
   root['true-child'] = SuperNode(function="x[1] == 12")
   root['false-child'] = SuperNode(value=0)
   
   root['true-child'].child_name_if_true = "true-grandchild"
   root['true-child'].child_name_if_false = "false-grandchild"
   root['true-child']["true-grandchild"] = SuperNode(value=1)
   root['true-child']["false-grandchild"] = SuperNode(value=2)
   
   value_1 = root.run_as_binary_tree(x=x1)
   print("Using x1 as input:")
   print(f"Value = {value_1.value}\n")
   
   value_2 = root.run_as_binary_tree(x=x2)
   print("Using x2 as input:")
   print(f"Value = {value_2.value}\n")
   