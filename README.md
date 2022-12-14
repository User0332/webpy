# WebPy

A web framework built on top of Flask that allows you to add filesystem routes (in the `root/` folder of your project directory).

## Commands

- `webpy new {proj-name}` - Create a new project
- `webpy route {route-name}` - Create a new filesystem route (this must be under `root/`)
- `webpy run` - Run this in the project dir to start your app using Flask

WebPy allows developers to use just a minimal amount of Python (the bare minimum needed) for their web apps while also allowing for the full functionality of Flask. Take a look at [webpy-app](https://github.com/User0332/webpy-app/) for example, where the majority of the codebase is HTML and JS while still allowing Flask to be fully utilized.
