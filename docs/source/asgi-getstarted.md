# Getting Started

## Installation
WebPy can be installed with `pip` using `pip install webpy-framework`. For a version that has not yet been published to PyPI (and therefore a version that may not necessarily work), the newest form of WebPy can be installed from the repository using `pip install git+https://github.com/User0332/webpy`. It requires at least Python 3.9, the version it was developed on.

## Your First WebPy Application

WebPy currently has a very minimal ASGI API (still in development). To start, import `App` from `webpy.asgi`. Then, use `app.route()` as you would with Flask, but this time the function should take in a `Request` and `Response` object. Use these to complete your response (see the below example).

```py
from webpy.asgi import App, Request, Response

app = App()

@app.route('/')
async def index(request: Request, response: Response):
    await request.start()
    await request.senddata("Hello, World!")

```

Save it in `app.py` and run the app with `uvicorn --host <your-host> --port <your-port> app:app`.