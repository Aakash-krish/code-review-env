import openenv

print([name for name in dir(openenv) if not name.startswith("_")])
if hasattr(openenv, "schema"):
    print(openenv.schema)
if hasattr(openenv, 'config'):
    print(dir(openenv.config))
