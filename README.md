# WebPy

A web framework built on top of Flask that allows you to add filesystem routes (in the `root/` folder of your project directory). Install it with `pip install webpy-framework`.

## Commands

### Creating your project
- `webpy new {proj-name}` - Create a new project
- `webpy route {route-name}` - Create a new filesystem route (this must be under `root/`)

### Deploying your project
- `webpy run` - Run this in the project dir to start your app using Flask
- `webpy build` - Package the program into a `build.py` file
- `webpy compile` - Package the program into a `build.pyc` file
- `webpy buildpyx` - Compile the `.pyx` files into `.py` files -- automatically runs through the `build`, `compile`, and `run` commands

WebPy allows developers to use just a minimal amount of Python (the bare minimum needed) for their web apps while also allowing for the full functionality of Flask. Take a look at [webpy-app](https://github.com/User0332/webpy-app/) for example, where the majority of the codebase is HTML and JS while still allowing Flask to be fully utilized. WebPy web servers can also be compiled to standalone exectuables by compiling the output of `webpy build` with a tool such as Nuitka.

### Your First WebPy Application

Start with `webpy new myfirstproject`. Then cd into the `myfirstproject` directory and open up your editor. It should look something like this:
```
myfirstproject/
  html/
  root/
    config.json
    index.py
  static/
    css/
      index.css
    images/
    js/
      index.js

  app.py
  config.json
```

The `app.py` file should contain some boilerplate code. You can use the `app` object just like a normal Flask object!. App configurations should be done inside the `webpy_setup` function. Route functions can still be created. The `config.json` file in the same directory as the `app.py` file configures how WebPy will run your app. It takes any arguments that are valid to pass to `app.run()`


Under `root/`, you can use `index.py` and `index.html` files to create filesystem-based webpage routes. If you use an `index.py` file, WebPy will call the `handler` function and pass the app as an argument. If you use `index.html`, WebPy will just return that HTML file to the requester. Each filesystem route has a `config.json` file. In this file, you can pass any keyword arguments that would be valid to pass to `app.route()`.

Let's create a new page at `http://127.0.0.1:5000/hello`. To do this, we can create a new folder called `hello/` under the `root/` folder. Cd into the `root/` directory and type `webpy route hello`. WebPy will automatically create the `hello/` directory for you.

```
myfirstproject/root/
  hello/
    index.py
    config.json

  ...
```

Since we only want this route to be a simple HTML page, we can delete `index.py` and replace it with `index.html`

`index.html`
```html
<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="/static/css/index.css"/>
	</head>
	<body>
		<h1 id="heading">Hello, World!</h1>
	</body>
</html>
```

Now, we can run our app using `webpy run`. Notice that when visiting `http://127.0.0.1:5000/hello`, the CSS that we linked from the `static/` folder is included.

If you want to make your app a little more compact, you can use `webpy build`. This will compile all of your Python and HTML into a single minifed file, `build.py`, which can be run like a normal Python script. However, the the `html/` and `static/` directories are not packaged into the build file, so these must still be present to run `build.py`. When using `webpy run`, changes in the files under `root/` and changes in files under `static/` are guaranteed to be reflected in the app without having to restart it, but if the app is being run from a `build.py`, changes in HTML, Python, and config files under `root/` will not be reflected.

[PyX](https://github.com/User0332/pyx) can also be integrated into WebPy apps by changing Python files to `.pyx` files. These files can be compiled to Python files using `webpy buildpyx`, which is automatically run by the `webpy build`, `webpy compile`, and `webpy run` commands. WebPy comes with PySite/PyX as a dependency.