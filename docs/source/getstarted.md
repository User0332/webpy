# Getting Started

## Installation
WebPy can be installed with `pip` using `pip install webpy-framework`. For a version that has not yet been published to PyPI (and therefore a version that may not necessarily work), the newest form of WebPy can be installed from the repository using `pip install git+https://github.com/User0332/webpy`. It requires at least Python 3.9, the version it was developed on.

## Your First WebPy Application

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

The `app.py` file should contain some boilerplate code. You can use the `app` object just like a normal Flask object! App configurations should be done inside the `webpy_setup` function. Route functions can still be created. The `config.json` file in the same directory as the `app.py` file configures how WebPy will run your app. It takes any arguments that are valid to pass to `app.run()`.


Under `root/`, you can use `index.py` and `index.html` files to create filesystem-based webpage routes. If you use an `index.py` file, WebPy will call the `handler` function and pass the app as an argument. If you use `index.html`, WebPy will just return that HTML file to the requester. Each filesystem route has a `config.json` file. In this file, you can pass any keyword arguments that would be valid to pass to `app.route()`.

Let's create a new page at `http://127.0.0.1:5000/hello`. To do this, we can create a new folder called `hello/` under the `root/` folder. Cd into the `root/` directory and type `webpy route hello`. WebPy will automatically create the `hello/` directory for you.

```
myfirstproject/root/
  hello/
    index.py
    config.json

  ...
```

Since we only want this route to be a simple HTML page, we can delete `index.py` and replace it with an `index.html` file.

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

If you want to make your app a little more compact, you can use `webpy build`. This will compile all of your Python and HTML into a single minifed file, `build.py`, which can be run like a normal Python script. However, the the `html/` and `static/` directories are not packaged into the build file, so these must still be present to run `build.py`. When using `webpy run` to run the app, changes in the files under `root/` and changes in files under `static/` are guaranteed to be reflected in the app without having to restart it, but if the app is being run from a `build.py` file, changes in HTML, Python, and config files under `root/` will not be reflected.

## Using PyX With WebPy

[PyX](https://github.com/User0332/pyx) can also be integrated into WebPy apps by changing Python files to `.pyx` files. These files can be compiled to Python files using `webpy buildpyx`, which is automatically run by the `webpy build`, `webpy compile`, and `webpy run` commands. WebPy comes with PySite/PyX as a dependency. Note that one must still import PySite HTML tags in every file that PyX is used, as shown below:
```py
from webpy.pysite_semantic_tags import * # recommended

### OR

from pysite.tags import * # also works, but doesn't filter out unnecessary classes such as Element
```

## Using Markdown With WebPy

Markdown written in `.md` files anywhere in the project are transpiled to `.html` files before running or building the project. They can also be transpiled using `webpy buildmd`. This means that Markdown can even be used in the `html/` directory and accessed as an HTML template. Markdown is placed in the body of the generated HTML document, so it will look something like this:

Markdown:
```md
# My Heading
```

HTML:
```html
<!DOCTYPE html>

<html>
    <head></head>

    <body>
        <h1>My Heading</h1>
    </body>
</html>
```

This feature currently uses the Python `marko` library, which supports CommonMark spec v0.30 (the latest version).
