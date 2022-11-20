import os
import json
from flask import Flask, render_template
from functools import partial

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
	

def parse_fs_routes(app: Flask, rootdir: str, parent: str='/') -> bool:
	conf = f"{rootdir}/config.json"
	index = f"{rootdir}/index.py"
	index_html = f"{rootdir}/index.html"
	
	if os.path.exists(conf):
		with open(conf, 'r') as f:
			try: config: dict = json.load(f)
			except json.decoder.JSONDecodeError:
				print(f"{conf} is invaliZd!")
				return False

	if os.path.exists(index):
		try:
			index = modularize(index)
		except Exception as e:
			print(f"{index} threw an error!\n{e}")
			return False

		if not hasattr(index, "handler"):
			print(f"{index} is missing a respond function!")
			return False

		handler = partial(index.handler, app)
		handler.__name__ = f"{parent}_handler"

		app.route(parent, **config)(handler)
	else:
		if not os.path.exists(index_html):
			print(f"{index} or {index_html} not found!")
			return False
		
		handler = partial(
			lambda fname: open(fname, 'r').read(), 
			index_html
		)
		handler.__name__ = f"{parent}_handler"

		app.route(parent, **config)(handler)

	for subdir in os.listdir(rootdir):
		sub_qual = f"{rootdir}/{subdir}"
		if os.path.isdir(sub_qual):
			if not parse_fs_routes(app, sub_qual, f"{parent}{subdir}/"):
				return False

	return True

