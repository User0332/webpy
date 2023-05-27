# WebPy Command Line

Running the command `webpy` will output a list of commands for the current version. Currently, the commands are: 

- `webpy new {proj-name}` - Create a new project with name `proj-name`
- `webpy route {route-name}` - Create a new filesystem route (this must be under `root/`) with name `route-name`
- `webpy run` - Run this in the project dir to start your app using Flask
- `webpy build` - Package the program into a `build.py` file
- `webpy compile` - Package the program into a `build.pyc` file
- `webpy buildpyx` - Compile the `.pyx` files into `.py` files -- automatically runs through the `build`, `compile`, and `run` commands