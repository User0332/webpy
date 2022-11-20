import os
from .fs_routes import parse_fs_routes
from flask import Flask
from json import load, dumps
from shutil import rmtree
from sys import argv
from importlib import import_module

if len(argv) < 2: exit(1)

defaultroutecode = """import webpy
from flask import Flask, request, render_template

def handler(app: Flask, *args):
	document = webpy.documentify("index.html")

	return document._stringify()
"""

defaultrouteconf = {
	"methods": ["GET"]
}

if argv[1] == "run":
	if os.path.exists("config.json"):
		with open("config.json", 'r') as f:
			conf: dict = load(f)

	app: Flask = import_module("app").app

	if not parse_fs_routes(app, "root"):
		exit(1)

	app.run(
		conf.get("host", "127.0.0.1"),
		conf.get("port", 5000)
	)

if argv[1] == "new":
	if len(argv) < 3:
		print("Missing project name!")
		exit(1)

	name = argv[2]

	if os.path.exists(name): rmtree(name)

	defaultconf = {
		"host": "127.0.0.1",
		"port": 5000
	}

	defaultcode = """from flask import Flask

app = Flask(__name__, template_folder="html")"""

	os.mkdir(name)

	os.mkdir(f"{name}/html")
	open(f"{name}/html/index.html", 'w').write(
		"""<!DOCTYPE html>
<html>
	<head>
		<script src="../static/js/index.js" defer></script>
		<link rel="stylesheet" href="../static/css/index.css"></link>
	</head>
	<body>
		<h1 id="heading"></h1>
	</body>
</html>"""
	)

	os.mkdir(f"{name}/static")

	os.mkdir(f"{name}/static/js")
	open(f"{name}/static/js/index.js", 'w').write(
		"""document.getElementById("heading")
	.textContent = "Hello World!"
"""
	)

	os.mkdir(f"{name}/static/css")
	open(f"{name}/static/css/index.css", 'w').write(
		"""#heading {
	color: red;
}"""
	)

	os.mkdir(f"{name}/static/images")

	open(f"{name}/app.py", 'w').write(
		defaultcode
	)

	open(f"{name}/config.json", 'w').write(
		dumps(defaultconf, indent='\t')
	)

	os.mkdir(f"{name}/root")
	open(f"{name}/root/config.json", 'w').write(
		dumps(defaultrouteconf, indent='\t')
	)

	open(f"{name}/root/index.py", 'w').write(
		defaultroutecode
	)

if argv[1] == "route":
	if len(argv) < 3:
		print("Missing route name!")
		exit(1)

	name = argv[2]

	if os.path.exists(name): rmtree(name)

	os.mkdir(f"{name}")
	open(f"{name}/config.json", 'w').write(
		dumps(defaultrouteconf, indent='\t')
	)

	open(f"{name}/index.py", 'w').write(
		defaultroutecode
	)


