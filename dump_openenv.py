import os
import openenv

openenv_dir = os.path.dirname(openenv.__file__)
for root, dirs, files in os.walk(openenv_dir):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            print(f"--- {f} ---")
            with open(path, 'r', encoding='utf-8') as fp:
                print(fp.read())
