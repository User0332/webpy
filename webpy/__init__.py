from flask import render_template
from domapi import make_document_from_str

def documentify(fname: str):
	return make_document_from_str(
		render_template(fname)
	)