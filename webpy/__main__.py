import os
import dill
import sys
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
from marko import convert as md_to_html
from argparse import ArgumentParser
from threading import Thread

WATCH_FILES: dict[str, int] = {}

def watch_md():
	while 1:
		for path, directories, files in os.walk(os.getcwd()):
			for file in files:
				file: str
				if file.endswith(".md"):
					actual =  os.path.join(path, file)

					mtime = os.stat(actual).st_mtime

					if WATCH_FILES[actual] != mtime:
						WATCH_FILES[actual] = mtime

						html = '\n\t\t'.join(
							md_to_html(open(actual, 'r').read())
							.splitlines()
						)

						print(f"webpy: detected change in {actual!r}, recompiling")

						with open(actual.removesuffix(".md")+".html", 'w') as f:
							f.write(
								f"""<!DOCTYPE html>
<html>
	<head></head>
	<body>
		{html}
	</body>
</html>
""")
						
def watch_pyx():
	while 1:
		shell = ["powershell"] if os.name == "nt" else ["bash", "-c"]
		for path, directories, files in os.walk(os.getcwd()):
			for file in files:
				file: str
				if file.endswith(".pyx"):
					actual =  os.path.join(path, file)

					mtime = os.stat(actual).st_mtime

					if WATCH_FILES[actual] != mtime:
						WATCH_FILES[actual] = mtime

						print(f"webpy: detected change in {actual!r}, reloading")

						subproc_call(
							[*shell, "pyxc", repr(actual)]
						)

def buildmd():
	for path, directories, files in os.walk(os.getcwd()):
		for file in files:
			file: str
			if file.endswith(".md"):
				actual =  os.path.join(path, file)
				html = '\n\t\t'.join(
					md_to_html(open(actual, 'r').read())
					.splitlines()
				)

				WATCH_FILES[actual] = os.stat(actual).st_mtime
				

				with open(actual.removesuffix(".md")+".html", 'w') as f:
					f.write(
						f"""<!DOCTYPE html>
<html>
	<head></head>
	<body>
		{html}
	</body>
</html>
""")

def build(force_debug: bool, compile_md: bool, compile_pyx: bool, deploying: bool=False):
	if compile_pyx: buildpyx()
	if compile_md: buildmd()

	conf = {}

	if os.path.exists("config.json"):
		with open("config.json", 'r') as f:
			conf: dict = load(f)

	sys.path.insert(0, os.getcwd()) # this is needed in case the script was run without `python -m`
	try: appmod = import_module("app")
	except ModuleNotFoundError:
		print("app.py file does not exist!")
		exit(1)
	
	try:
		app: Flask = appmod.app
		setup: FunctionType = appmod.webpy_setup
	except AttributeError:
		print("app object and webpy_setup function are missing from app.py!")

	prerules = list(app.url_map.iter_rules())

	# TODO: use TypedDict for this
	routes: dict[str, dict[str, Union[dict[str, str], bytes, str]]] = {}

	if not parse_fs_routes(app, "root", routes, {}):
		exit(1)

	with open("build.py", 'w') as f:
		code = ""
		for module in conf.get("imports", tuple()):
			code+=f"import {module}\n"

		code+=(
			f"""from dill import loads
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

loads({dill.dumps(setup)!r})(app)
app.debug = {True if force_debug else False}
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
					f"route({route!r}, {','.join(f'{key}={value!r}' for key, value in config.items())})"
					f"(appbind(lambda _: {handler!r}, "
					f"app, {route+'_handler'!r}))\n"
				)

				continue
			
			code+=(
				f"route({route!r}, {','.join(f'{key}={value!r}' for key, value in config.items())})"
				f"(appbind(loads({handler!r}), "
				f"app, {route+'_handler'!r}))\n"
			)

		if not deploying: code+=(f"app.run({','.join(f'{key}={value!r}' for key, value in conf.items())})")

		f.write(minify(code, rename_globals=True) if not deploying else minify(code))

def run(
		force_debug: bool,
		compile_md: bool,
		compile_pyx: bool,
		reload_md: bool,
		reload_pyx: bool
	):
	
	if compile_pyx: buildpyx()
	if compile_md: buildmd()

	conf = {}

	if os.path.exists("config.json"):
		with open("config.json", 'r') as f:
			conf: dict = load(f)

	sys.path.insert(0, os.getcwd()) # this is needed in case the script was run without `python -m`
	try: appmod = import_module("app")
	except ModuleNotFoundError:
		print("app.py file does not exist!")
		exit(1)
	
	try:
		app: Flask = appmod.app
		setup: FunctionType = appmod.webpy_setup
	except AttributeError:
		print("app object and webpy_setup function are missing from app.py!")

	if force_debug: app.debug = True

	routes = {}

	setup(app)

	if not parse_fs_routes(app, "root", WATCH_FILES, routes):
		exit(1)

	if reload_md and compile_md:
		t = Thread(target=watch_md)
		t.daemon = True
		t.start()

	if reload_pyx and app.debug and compile_pyx:
		t = Thread(target=watch_pyx)
		t.daemon = True
		t.start()
		
	app.run(**conf)

def new(name: str):
	if os.path.exists(name): rmtree(name)

	defaultconf = {
		"host": "127.0.0.1",
		"port": 5000
	}

	defaultcode = """from webpy import App

app = App(__name__, template_folder="html")

def webpy_setup(app: App):
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

def route(name: str):
	if os.path.exists(name): rmtree(name)

	os.mkdir(f"{name}")
	open(f"{name}/config.json", 'w').write(
		dumps(defaultrouteconf, indent='\t')
	)

	open(f"{name}/index.py", 'w').write(
		defaultroutecode
	)

def webpy_compile(force_debug: bool, compile_md: bool, compile_pyx: bool, deploying: bool=False):
	build(force_debug, compile_md, compile_pyx, deploying=deploying)

	compile("build.py", "build.pyc", optimize=2)

	try: os.remove("build.py")
	except FileNotFoundError: pass

def deploy(force_debug: bool, compile_md: bool, compile_pyx: bool):
	print("creating build.pyc...")
	webpy_compile(force_debug, compile_md, compile_pyx, deploying=True)
	print("done creating build.pyc")

	print("starting app with waitress...")

	conf: dict[str] = {}

	if os.path.exists("config.json"):
		with open("config.json", 'r') as f:
			conf = load(f)

	try: subproc_call(
		[
			"waitress-serve",
			"--host", str(conf.get("host", "127.0.0.1")),
			"--port", str(conf.get("port", 5000)),
			"build:app"
		]
	)
	except KeyboardInterrupt: pass

def buildpyx():
	shell = ["powershell"] if os.name == "nt" else ["bash", "-c"]

	for path, directories, files in os.walk(os.getcwd()):
		for file in files:
			file: str
			if file.endswith(".pyx"):
				actual =  os.path.join(path, file)

				WATCH_FILES[actual] = os.stat(actual).st_mtime

				subproc_call(
					[*shell, "pyxc", repr(actual)]
				)

if len(argv) < 2: argv.append('')

defaultroutecode = """import webpy

def handler(app: webpy.App, *args):
	from flask import request
	
	document = webpy.documentify("index.html")

	return document._stringify()
"""

defaultrouteconf = {
	"methods": ["GET"]
}

def main():
	parser = ArgumentParser("webpy", description="CLI for the webpy framework (docs: https://webpy-framework.readthedocs.io/)")
	parser.add_argument(
		"command", 
		choices=(
		"run",
		"build",
		"new",
		"route",
		"compile",
		"buildpyx",
		"buildmd",
		"show",
		"deploy"
		),
		help="Possible commands --- webpy new {projectname} (create a new project) --- webpy route {routename} (create a new route directory) --- webpy run (start the application) --- webpy build (compile root/ and app.py into build.py) --- webpy compile (like build but create build.pyc) --- webpy buildpyx (compile all .pyx to .py) --- webpy buildmd (compile all .md to .html) --- webpy show <info> (show info about the app) --- webpy deploy (deploy the app using Waitress)"
	)

	parser.add_argument("name", help="name to be used for 'new' or 'route' commands", default=None, nargs='?')

	parser.add_argument("--no-compile-md", action="store_true", help="do not compile Markdown to HTML")
	parser.add_argument("--no-compile-pyx", action="store_true", help="do not compile PyX to Python")
	parser.add_argument("--no-reload-md", action="store_true", help="do not check for modifications in Markdown files while running")
	parser.add_argument("--no-reload-pyx", action="store_true", help="do not check for modifications in PyX files while running")
	parser.add_argument("--force-debug", action="store_true", help="make sure debug mode is used")


	args = parser.parse_args()
	cmd = args.command
	name = args.name

	compile_md = not args.no_compile_md
	compile_pyx = not args.no_compile_pyx
	reload_md = not args.no_reload_md
	reload_pyx = not args.no_reload_pyx
	force_debug = args.force_debug

	if cmd == "run":
		run(
			force_debug,
			compile_md,
			compile_pyx,
			reload_md,
			reload_pyx
		)
		exit(0)

	if cmd == "build":
		build(
			force_debug,
			compile_md,
			compile_pyx,
		)
		exit(0)

	if cmd == "new":
		if not name:
			print("webpy: error: expected name to be used with 'new'")
			exit(1)

		new(name)
		exit(0)

	if cmd == "route":
		if not name:
			print("webpy: error: expected name to be used with 'route'")
			exit(1)
			
		route(name)
		exit(0)

	if cmd == "compile":
		webpy_compile(force_debug, compile_md, compile_pyx)
		exit(0)

	if cmd == "buildpyx":
		buildpyx()
		exit(0)

	if cmd == "buildmd":
		buildmd()
		exit(0)

	if cmd == "show":
		if name not in ("routes", "overview"):
			print("webpy: error: expected extra command name to be used with 'show'\n  e.g.\n\tshow routes - view application routes\n\tshow overview - view config, app properties, and config stats")
			exit(1)
		pass

	if cmd == "deploy":
		deploy(force_debug, compile_md, compile_pyx)
		exit(0)

if __name__ == "__main__":
	main()