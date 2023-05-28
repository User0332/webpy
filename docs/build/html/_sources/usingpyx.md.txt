# Using PyX With WebPy

[PyX](https://github.com/User0332/pyx) can also be integrated into WebPy apps by changing Python files to `.pyx` files. These files can be compiled to Python files using `webpy buildpyx`, which is automatically run by the `webpy build`, `webpy compile`, and `webpy run` commands. WebPy comes with PySite/PyX as a dependency. Note that one must still import PySite HTML tags in every file that PyX is used, as shown below:
```py
from webpy.pysite_semantic_tags import * # recommended

### OR

from pysite.tags import * # also works, but doesn't filter out unnecessary classes such as Element
```

## PyX Snippets

PyX snippets can also be imported from `webpy.pyx_snippets`. Currently, the only snippet available is `theme`, which takes in one attribute name of `name={theme-name}`. These themes are fetched from [User0332.github.io/tree/main/webpy/themes](https://github.com/User0332/User0332.github.io/tree/main/webpy/themes).
