import webpy
from flask import Flask, request, render_template

def handler(app: Flask, *args):
	return f"<h1>You are in the Hello API - {request.json}</h1>"
