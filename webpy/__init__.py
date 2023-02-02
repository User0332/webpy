from flask import render_template, Flask
from functools import partial
from types import FunctionType
from domapi import make_document_from_str

def documentify(fname: str):
	return make_document_from_str(
		render_template(fname)
	)

def appbind(func: FunctionType, app: Flask, name: str):
	new = partial(func, app)
	new.__name__ = name

	return new