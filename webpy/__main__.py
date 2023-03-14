import os
import dill
from .fs_routes import parse_fs_routes
from flask import Flask
from py_compile import compile
from python_minifier import minify
from json import load, dumps
from shutil import rmtree
from sys import argv
from importlib import import_module
from typing import Union
from subprocess import call as subproc_call
from types import FunctionType

def build():
	buildpyx()

	conf = {}

	if os.path.exists("config.json"):
		with open("config.json", 'r') as f:
			conf: dict = load(f)

	appmod = import_module("app")
	app: Flask = appmod.app
	setup: FunctionType = appmod.webpy_setup

	prerules = list(app.url_map.iter_rules())

	# TODO: use TypedDict for this
	routes: dict[str, dict[str, Union[dict[str, str], bytes, str]]] = {}

	if not parse_fs_routes(app, "root", routes):
		exit(1)

	host, port = conf.get("host", "127.0.0.1"), conf.get("port", 5000)

	with open("build.py", 'w') as f:
		code = ""
		for module in conf.get("imports", tuple()):
			code+=f"import {module}\n"

		code+=(
			f"""import dill
from webpy import appbind
from flask import Flask

app = Flask(
	{app.import_name!r},
	{app.static_url_path!r},
	{app.static_folder!r},
	{conf.get("static_host", None)!r},
	{app.url_map.host_matching!r},
	{app.subdomain_matching!r},
	{app.template_folder!r},
	{app.instance_path!r},
	{conf.get("instance_relative_config", False)!r},
	{app.root_path!r}
)

dill.loads({dill.dumps(setup)!r})(app)
"""
		)

		for rule in prerules:
			if rule.endpoint == "static": continue
			
			code+=(
				f"""
app.add_url_rule(
	{rule.rule!r}, 
	{rule.endpoint!r},
	dill.loads({dill.dumps(app.view_functions[rule.endpoint])!r}),
	methods={list(rule.methods)!r},
	defaults={rule.defaults!r},
	subdomain={rule.subdomain!r},
	build_only={rule.build_only!r},
	strict_slashes={rule.strict_slashes!r},
	merge_slashes={rule.merge_slashes!r},
	redirect_to=dill.loads({dill.dumps(rule.redirect_to)!r}),
	alias={rule.alias!r},
	host={rule.host!r},
	websocket={rule.websocket!r}
)	
"""
			)

		code+="route = app.route\n"

		for route, routeobj in routes.items():
			config, handler = routeobj.values()

			if routeobj.get("statichtml") is not None:
				code+=(
					f"route({route!r}, **{config})"
					f"(appbind(lambda _: {handler!r}, "
					f"app, {route+'_handler'!r}))\n"
				)

				continue
			
			code+=(
				f"route({route!r}, **{config})"
				f"(appbind(dill.loads({handler!r}), "
				f"app, {route+'_handler'!r}))\n"
			)

		code+=(f"app.run({host!r}, {port!r})")

		f.write(minify(code, rename_globals=True))

def run():
	buildpyx()

	conf = {}

	if os.path.exists("config.json"):
		with open("config.json", 'r') as f:
			conf: dict = load(f)

	appmod = import_module("app")
	app: Flask = appmod.app
	setup: FunctionType = appmod.webpy_setup

	routes = {}

	setup(app)

	if not parse_fs_routes(app, "root", routes):
		exit(1)

	host, port = conf.get("host", "127.0.0.1"), conf.get("port", 5000)

	app.run(host, port)

def new():
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

app = Flask(__name__, template_folder="html")

def webpy_setup(app: Flask):
	app.debug = True"""

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

def route():
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

def webpy_compile():
	build()
	compile("build.py", "build.pyc", optimize=2)

	try: os.remove("build.py")
	except FileNotFoundError: pass

def buildpyx():
	shell = ["powershell"] if os.name == "nt" else ["bash", "-c"]

	for path, directories, files in os.walk(os.getcwd()):
		for file in files:
			file: str
			if file.endswith(".pyx"):
				actual =  os.path.join(path, file)

				subproc_call(
					[*shell, "pyxc", actual]
				)

if len(argv) < 2: argv.append('')

defaultroutecode = """import webpy
from flask import Flask

def handler(app: Flask, *args):
	from flask import request
	
	document = webpy.documentify("index.html")

	return document._stringify()
"""

defaultrouteconf = {
	"methods": ["GET"]
}

if argv[1] == "run":
	run()
	exit(0)

if argv[1] == "build":
	build()
	exit(0)

if argv[1] == "new":
	new()
	exit(0)

if argv[1] == "route":
	route()
	exit(0)

if argv[1] == "compile":
	webpy_compile()
	exit(0)

if argv[1] == "buildpyx":
	buildpyx()
	exit(0)

print(f"Invalid command {repr(argv[1]) if argv[1] else '<none>'}")
print("Possible commands:\n- webpy new {projectname}\n- webpy route {routename}\n- webpy run\n- webpy build\n- webpy compile\n- webpy buildpyx")