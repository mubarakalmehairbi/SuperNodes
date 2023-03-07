import glob
import os
import subprocess
import sys
sys.path.insert(0, "..")
import inspect
from pythontrees import DataNode, InEquality

package_title = "PythonTrees"
classes = [DataNode, InEquality]
examples = glob.glob("../examples/*.py")
sections = {"Classes": [f"{cls.__module__}.{cls.__name__}" for cls in classes]}
clear = True
run = True

if clear:
    for file in glob.glob("*.rst"):
        if not "template.rst" in file:
            os.remove(file)

def replace_template(dictionary, rst_template, new_rst_file):
    with open("_my_templates/" + rst_template, "rt") as template:
        text = template.read()
        for key, value in dictionary.items():
            text = text.replace("{{" + key + "}}", value)
    with open(new_rst_file, "w") as new_file:
        new_file.write(text)

index_dict = {"title": package_title,
              "under_title":len(package_title)*"=","contents": "\n   ".join(list(sections.keys()))}
replace_template(index_dict, "index_template.txt", "index.rst")

for section_title, section_contents in sections.items():
    contents = "\n   ".join(section_contents)
    classes_section_dict = {"title": section_title,
                            "under_title": len(section_title)*"=",
                            "contents": contents}
    replace_template(classes_section_dict, "section_template.txt", f"{section_title}.rst")

for cls in classes:
    cls_api = f"{cls.__module__}.{cls.__name__}"
    methods = [f for f in inspect.getmembers(cls, inspect.isfunction) if not f[0].startswith("_")]
    methods_str = "\n   ".join([f"{cls_api}.{m[0]}" for m in methods])
    cls_dict = {"class_name": cls.__name__,
                "under_class_name": "="*len(cls.__name__),
                "to_class": cls_api,
                "methods": f"{methods_str}"}
    replace_template(cls_dict, "class_template.txt", f"{cls_api}.rst")
    for method_name, method in methods:
        method_api = f"{cls_api}.{method_name}"
        method_dict = {"method_name": f"{cls.__name__}.{method_name}",
                       "under_method_name": "-"*len(f"{cls.__name__}.{method_name}"),
                       "to_method": method_api}
        replace_template(method_dict, "method_template.txt", f"{method_api}.rst")

#for example in examples:
#    title = os.path.basename(example).removesuffix('.py')
#    example_dict = {"title": title,
#                    "under_title": len(title)*"=",
#                    "path": example}
#    replace_template(example_dict, "code_template.txt", f"{title}.rst")

if run:
    subprocess.check_call(['make', 'clean'])
    subprocess.check_call(['make', 'html'])
