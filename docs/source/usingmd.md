# Using Markdown With WebPy

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
