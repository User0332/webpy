# Application Routes

As you saw in [Get Started](getstarted.md), routes in WebPy can be created in a few different ways.

## Filesystem Routes

Filesystem-based routes use directory/path names to place themselves on the app. The directories for these routes will be under the `root/` folder, which itself corresponds to the route `/`. In order to create a new route, use the `webpy route <routename>` command. A more visual example of how directories correspond to app routes is shown below.

Assuming the app is running on `127.0.0.1:5000`,
```
appdirectory/root/      [127.0.0.1:5000/]
  hello/                [127.0.0.1:5000/hello]
    world/              [127.0.0.1:5000/hello/world]
  login/                [127.0.0.1:5000/login]
  
```

### HTML

To create a filesystem route that serves a static HTML file, use `webpy route` to create the route, delete the generated `index.py` file in the route directory, and replace it with `index.html`. Write your new HTML in `index.html`.

### Python

To create a programmed filesystem route, use the `webpy route` command to create the route and write your route code in the `handler(app, *args)` function of the generated `index.py` file.
Imports from `flask` should typically be inside of the handler function. The WebPy application object is passed as an argument (`app`).

### PyX

To create a programmed filesystem route that uses [PyX](https://github.com/User0332/pyx), you can again use the `webpy route` function, but this time rename `index.py` to `index.pyx`. WebPy will automatically compile all `.pyx` files to `.py` files before running. Don't forget to import PySite tags for PyX (see [Using PyX With WebPy](getstarted.md#using-pyx-with-webpy)).

## Flask Routes

To create a traditionally programmed Flask route, error handler, or URL rule with WebPy, you can use the same code that you would use for your Flask route, placing it in `app.py`. You can also integrate PyX into `app.py` by renaming it to `app.pyx`.