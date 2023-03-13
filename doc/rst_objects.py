import ast
import inspect
import os
from dataclasses import dataclass


@dataclass
class Index:

    package_title: str
    sections: list
    readme_path: str = None

    def to_rst(self):
        index_dict = {"title": self.package_title,
                      "under_title": len(self.package_title) * "=",
                      "contents": "\n   ".join([s.title for s in self.sections])}
        if self.readme_path:
            index_dict['read_me'] = f".. include:: {self.readme_path}\n   :parser: myst_parser.sphinx_"
        else:
            index_dict['read_me'] = ""
        replace_template(index_dict, "index_template.txt", "index.rst")


@dataclass
class Section:

    title: str
    children_rst: list
    text: str = ""

    def to_rst(self):
        contents = "\n   ".join(self.children_rst)
        text = self.text
        section_dict = {"title": self.title,
                                "under_title": len(self.title) * "=",
                                "text": text,
                                "contents": contents}
        replace_template(section_dict, "section_template.txt", f"{self.title}.rst")


class Class:


    def __init__(self, cls):
        self.cls = cls
        self.cls_api = f"{self.cls.__module__}.{self.cls.__name__}"

    def to_rst(self):
        cls_api = f"{self.cls.__module__}.{self.cls.__name__}"
        methods = [f for f in inspect.getmembers(self.cls, inspect.isfunction) if not f[0].startswith("_")]
        methods_str = "\n   ".join([f"{cls_api}.{m[0]}" for m in methods])
        cls_dict = {"class_name": self.cls.__name__,
                    "under_class_name": "=" * len(self.cls.__name__),
                    "to_class": cls_api,
                    "methods": f"{methods_str}"}
        if methods != []:
            replace_template(cls_dict, "class_template.txt", f"{cls_api}.rst")
        else:
            replace_template(cls_dict, "class_methodless_template.txt", f"{cls_api}.rst")
        for method_name, method in methods:
            method_api = f"{cls_api}.{method_name}"
            method_dict = {"method_name": f"{self.cls.__name__}.{method_name}",
                           "under_method_name": "-" * len(f"{self.cls.__name__}.{method_name}"),
                           "to_method": method_api}
            replace_template(method_dict, "method_template.txt", f"{method_api}.rst")


class Example:

    title: str = None
    path: str
    text: str = None

    def __init__(self, path, title=None, text=None):
        with open(path, "rt") as file:
            content = file.read()
            module = ast.parse(content, type_comments=True)
        docstring = ast.get_docstring(module).strip().splitlines()
        docstring_line_0 = docstring[0]
        self.path = path
        if title:
            self.title = title
        else:
            self.title = docstring_line_0
        if text:
            self.text = text
        else:
            self.text = "\n".join(docstring[1:]).strip()
        self.code = ""
        starting_line_num = module.body[1].lineno
        lines = content.splitlines()
        for line in lines[starting_line_num:]:
            self.code += line + "\n" + "   "

    def to_rst(self):
        self.rst = f"Examples.{os.path.basename(self.path).removesuffix('.py')}"
        example_dict = {"title": self.title,
                        "under_title": len(self.title) * "=",
                        "code": self.code,
                        "text": self.text,
                        "path": self.path}
        replace_template(example_dict, "code_template.txt", f"{self.rst}.rst")


def replace_template(dictionary, rst_template, new_rst_file):
    with open("_my_templates/" + rst_template, "rt") as template:
        text = template.read()
        for key, value in dictionary.items():
            text = text.replace("{{" + key + "}}", value)
    with open(new_rst_file, "w") as new_file:
        print(f"WRITING: {new_rst_file}")
        new_file.write(text)