# Using PyX With WebPy

[PyX](https://github.com/User0332/pyx) can also be integrated into WebPy apps by changing Python files to `.pyx` files. These files can be compiled to Python files using `webpy buildpyx`, which is automatically run by the `webpy build`, `webpy compile`, and `webpy run` commands. WebPy comes with PySite/PyX as a dependency. Note that one must still import PySite HTML tags in every file that PyX is used, as shown below:
```py
from webpy.pysite_semantic_tags import * # recommended

### OR

from pysite.tags import * # also works, but doesn't filter out unnecessary classes such as Element
```

## PyX Snippets

PyX snippets can also be imported from `webpy.pyx_snippets`. Currently, the only snippet available is `theme`, which takes in one attribute name of `name={theme-name}`. These themes are CSS and JavaScript files fetched from [User0332.github.io/tree/main/webpy/themes](https://github.com/User0332/User0332.github.io/tree/main/webpy/themes). Including the `theme` tag in your PyX document just fetches and links the associated `.css` and `.js` files.

## Example PyX Integration

Start by renaming the `index.py` file in your route to `index.pyx`. Then, you can write your PyX document just like you would write it in PySite. Let's start by adding our boilerplate.

`index.pyx`
```py
import webpy
from webpy.pysite_semantic_tags import *

def handler(app: webpy.App, *args):
  return (
    <pyx>

    </pyx>
  ).html
```

Then, lets add an `h1`, a `button`, and a `p` tag.

`index.pyx`
```py
import webpy
from webpy.pysite_semantic_tags import *

def handler(app: webpy.App, *args):
  return (
    <pyx>
+       <h1>Welcome to my site!</h1>
+       <p>This site was built using WebPy!</p>
+       <button onclick="alert('hello there!')"><h3>Click Me!</h3></button>
    </pyx>
  ).html
```

Run the app using `webpy run` and visit your route. Right now, the page doesn't look too good, but we can make it look much better with only a couple of lines of code.

We can do this by using WebPy PyX theme snippets. Import the `theme` snippet from `webpy.pyx_snippets`.

`index.pyx`
```py
import webpy
from webpy.pysite_semantic_tags import *
+ from webpy.pyx_snippets import theme

def handler(app: webpy.App, *args):
  return (
    <pyx>
        <h1>Welcome to my site!</h1>
        <p>This site was built using WebPy!</p>
        <button onclick="alert('hello there!')"><h3>Click Me!</h3></button>
    </pyx>
  ).html
```

Then, add the `theme` tag at the top of your document and give it a theme name. For now, we'll use the `webpy-bluepurple` theme.

`index.pyx`
```py
import webpy
from webpy.pysite_semantic_tags import *
from webpy.pyx_snippets import theme

def handler(app: webpy.App, *args):
  return (
    <pyx>
+       <theme name="webpy-bluepurple"></theme>
        <h1>Welcome to my site!</h1>
        <p>This site was built using WebPy!</p>
        <button onclick="alert('hello there!')"><h3>Click Me!</h3></button>
    </pyx>
  ).html
```

Run your app with the themes applied! Read more about the theme snippet [here](#pyx-snippets).