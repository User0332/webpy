import os
import json
import dill
from . import appbind
from flask import Flask

ROUTE_FUNCS = {}

class Module: pass

def modularize(file: str):
	mod = Module()

	with open(file, 'r') as f:
		code = f.read()

	exec(
		code,
		mod.__dict__
	)

	return mod
	

def parse_fs_routes(app: Flask, rootdir: str, routedict: dict, watchfiles: dict[str, int], parent: str='/') -> bool:
	conf = f"{rootdir}/config.json"
	index = f"{rootdir}/index.py"
	index_html = f"{rootdir}/index.html"
	
	if os.path.exists(conf):
		with open(conf, 'r') as f:
			try: config: dict = json.load(f)
			except json.decoder.JSONDecodeError:
				print(f"{conf} is invaliZd!")
				return False
	else: config = {}

	if os.path.exists(index):
		watchfiles[index] = os.stat(index).st_mtime
		try:
			index = modularize(index)
		except Exception as e:
			print(f"{index} threw an error!\n{e}")
			return False

		if not hasattr(index, "handler"):
			print(f"{index} is missing a handler function!")
			return False

		handler = appbind(
			index.handler,
			app,
			f"{parent}_handler"
		)

		routedict[parent] = {
			"config": config,
			"handler": dill.dumps(index.handler)
		}

		app.route(parent, **config)(handler)
	else:
		if not os.path.exists(index_html):
			print(f"{index} or {index_html} not found!")
			return False

		handler = lambda: open(index_html, 'r').read()
		handler.__name__ = f"{parent}_handler"
		
		routedict[parent] = {
			"config": config,
			"statichtml": handler()
		}

		app.route(parent, **config)(handler)


	for subdir in os.listdir(rootdir):
		sub_qual = f"{rootdir}/{subdir}"
		if os.path.isdir(sub_qual):
			if not parse_fs_routes(app, sub_qual, routedict, watchfiles, f"{parent}{subdir}/"):
				return False

	return True

