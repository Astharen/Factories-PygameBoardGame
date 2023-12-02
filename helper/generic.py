import importlib


def instance_class_from_module_and_name(module_name, class_name, **class_kwargs):
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    instance = class_(**class_kwargs)
    return instance


def snake_to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))
