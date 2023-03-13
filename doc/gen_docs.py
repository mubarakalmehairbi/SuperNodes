import glob
import os
import subprocess
from supernodes import SuperNode, InEquality
from rst_objects import Index, Section, Class, Example

clear = True
run = True

if clear:
    for file in glob.glob("*.rst"):
        if not "template.rst" in file:
            os.remove(file)

classes = []
for cls in (SuperNode, InEquality):
    cls_object = Class(cls)
    cls_object.to_rst()
    classes.append(cls_object)

examples = []
examples_paths = glob.glob("../examples/*.py")
for example in examples_paths:
    example_object = Example(path=example)
    example_object.to_rst()
    examples.append(example_object)


sections = []
section_api = Section(title="API Reference", children_rst=[cls.cls_api for cls in classes],
                  text="Here you can find the classes you can use in this package.")
section_api.to_rst()
sections.append(section_api)

section_examples = Section(title="Examples", children_rst=[e.rst for e in examples],
                           text="Here you can find some examples on using the package.")
section_examples.to_rst()
sections.append(section_examples)


index = Index(package_title="SuperNodes", readme_path="../README.md", sections=sections)
index.to_rst()


if run:
    subprocess.check_call(['make', 'clean'])
    subprocess.check_call(['make', 'html'])
