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

Lets modify our default route under `http://127.0.0.1:5000/`, in the directory `root/`. This time, we'll keep `index.py` and program this route in Python. The default code should look something like this:

`index.py`
```py
import webpy

def handler(app: webpy.App, *args):
	from flask import request
	
	document = webpy.documentify("index.html")

	return document._stringify()
```

Right now, the code reads `index.html` from the `html/` folder and turns it into a document object using [`domapi`](https://github.com/User0332/domapi). It then returns the string form of the document. However, the `handler()` function that we see here can return strings and `flask.Response` objects too (see [Python routes](routes.md#python)). Let's start with a simple example and use a string.

First, delete the default route code.

`index.py`
```py
import webpy

def handler(app: webpy.App, *args):

```

Then, return a string of HTML from the function.

`index.py`
```py
import webpy

def handler(app: webpy.App, *args):
+ return "<h1>Hello, World!</h1>"
```

Start the app again using `webpy run`, and we can see our `h1` show up on `http://127.0.0.1:5000/`. For more information on how you can use programmed routes, visit the [Flask documentation](https://flask.palletsprojects.com/en/2.3.x/quickstart/) or take a look at some [examples](https://github.com/User0332/webpy-app/tree/master/root).
