# Deploying Your Application

# WebPy Build

If you want to make your app a little more compact, you can use `webpy build`. This will compile all of your Python and HTML into a single minifed file, `webpy_build.py`, which can be run like a normal Python script. However, the the `html/` and `static/` directories are not packaged into the build file, so these must still be present to run `webpy_build.py`. When using `webpy run` to run the app, changes in the files under `root/` and changes in files under `static/` are guaranteed to be reflected in the app without having to restart it, but if the app is being run from a `webpy_build.py` file, changes in HTML, Python, and config files under `root/` will not be reflected.

# Deployment Server

Running the command `webpy deploy` in your project directory will compile a `webpy_build.pyc` and will start your app using the Waitress WSGI server.