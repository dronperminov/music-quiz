from jinja2 import Environment, FileSystemLoader

templates = Environment(loader=FileSystemLoader("web/templates"), cache_size=0)
templates.policies["json.dumps_kwargs"]["ensure_ascii"] = False
