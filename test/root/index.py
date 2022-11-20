import webpy
from flask import Flask, request, render_template

def handler(app: Flask, *args):
	document = webpy.documentify("index.html")

	elem = document.createElement("h2")
	# can't use innerHTML, innerText, or textContent currently
	elem._root.text = "this is an h2!"

	style = document.createAttribute("style")
	style.value = "color: green;"
	elem.attributes.setNamedItem(style)

	document.body.append(elem)

	return document._stringify()
