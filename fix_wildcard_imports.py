import re
import sys


def fix_imports(import_str):
    match = re.search("from (.*) import \*",  import_str)
    if not match:
        return import_str

    module = match.groups()[0]
    try:
        __import__(module)
    except ImportError as e:
       # print e
       return import_str
    imported_module = sys.modules[module]
    if hasattr(imported_module, "__all__"):
        module_attrs = imported_module.__all__
    else:
        module_attrs = [attr for attr in dir(imported_module)
                        if not attr.startswith("_")]

    return re.sub("import \*", "import " + ", ".join(module_attrs), import_str)




if __name__ == "__main__":
    if not sys.argv[1:]:
        print "Usage: \n\t python %s path/to/python/file.py" % sys.argv[0]
        sys.exit(1)

    f = sys.argv[1]
    f_path = re.sub("\w*.py", "", f)
    sys.path.append(f_path)

    import fileinput
    for line in fileinput.FileInput(f, inplace=1):
        print fix_imports(line),
