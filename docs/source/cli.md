# WebPy Command Line


## Commands

Running the command `webpy -h` will output a list of commands for the current version. Currently, the commands are: 

- `webpy new {proj-name}` - Create a new project with name `proj-name`
- `webpy route {route-name}` - Create a new filesystem route (this must be under `root/`) with name `route-name`
- `webpy run` - Run this in the project dir to start your app using Flask
- `webpy build` - Package the program into a `build.py` file
- `webpy compile` - Package the program into a `build.pyc` file
- `webpy buildpyx` - Compile the `.pyx` files into `.py` files -- automatically runs through the `build`, `compile`, and `run` commands
- `webpy buildmd` - Transpile all Markdown files to HTML

## Options

- `--no-compile-md` - Do not transpile Markdown to HTML when running/building
- `--no-compile-pyx` - Do not transpile PyX to Python when running/building
- `--no-reload-md` - When running the app, do not re-transpile Markdown files if changes are detected (this is auto-set if `--no-compile-md` is set)
- `--no-reload-pyx` - When running the app, do not re-transpile PyX files if changes are detected (this is auto-set if `--no-compile-pyx` is set)
- `--force-debug` - Force the application to use debug mode when running/building