# WebPy

A web framework built on top of Flask that allows you to add filesystem routes (in the `root/` folder of your project directory).

## Commands

NOTE: Commands may have to be invoked via `python -m webpy` if an alias for WebPy is not created.

### Creating your project
- `webpy new {proj-name}` - Create a new project
- `webpy route {route-name}` - Create a new filesystem route (this must be under `root/`)

### Deploying your project
- `webpy run` - Run this in the project dir to start your app using Flask
- `webpy build` - Package the program into a `build.py` file
- `webpy compile` - Package the program into a `build.pyc` file
- `webpy buildpyx` - Compile the `.pyx` files into `.py` files -- automatically runs through the `build`, `compile`, and `run` commands

WebPy allows developers to use just a minimal amount of Python (the bare minimum needed) for their web apps while also allowing for the full functionality of Flask. Take a look at [webpy-app](https://github.com/User0332/webpy-app/) for example, where the majority of the codebase is HTML and JS while still allowing Flask to be fully utilized. WebPy web servers can also be compiled to standalone exectuables by compiling the output of `webpy build` with a tool such as Nuitka.
