# Debug Reloading

## Python Files

When `app.debug = True`, Flask automatically reloads all Python files if changes are detected. This flag can also be set using [`--force-debug`](cli.md#options) (`webpy build` will assume no debug mode, but `--force-debug` will make sure it uses debug mode).

## PyX and Markdown Files

When the `--no-reload-XX` flags AND the `--no-compile-XX` flags are not set, WebPy will re-transpile the XX filetype IF `app.debug = True`. 

Ex. if both `--no-reload-pyx` and `--no-compile-pyx` are not set and the app is in debug mode, any changes in PyX files will be transpiled to Python and reflected in the application. An example command that will make sure that PyX, Markdown, AND Python is reloaded would look like this: `webpy run --force-debug`.

## HTML Files

HTML files under the `root/` directory will always have their changes reflected instantly (on the next reload of the webpage), regardless of the `app.debug` value. This does not apply to packaged `build.py` files or HTML files under the `html/` directory.