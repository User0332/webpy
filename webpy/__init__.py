import os
import typing as t
from flask import render_template, Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
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
	
class App(Flask):
	def __init__(
		self,
		import_name: str,
		static_url_path: t.Optional[str] = None,
		static_folder: t.Optional[t.Union[str, os.PathLike]] = "static",
		static_host: t.Optional[str] = None,
		host_matching: bool = False,
		subdomain_matching: bool = False,
		template_folder: t.Optional[str] = "templates",
		instance_path: t.Optional[str] = None,
		instance_relative_config: bool = False,
		root_path: t.Optional[str] = None
	):
		super().__init__(
			import_name, 
			static_url_path, 
			static_folder, 
			static_host, 
			host_matching, 
			subdomain_matching, 
			template_folder,
			instance_path,
			instance_relative_config,
			root_path
		)

		self.sqlalchemy = SQLAlchemyWrapper(self)

	def session(self: Flask, sess_type: str="filesystem", sess_permanent: bool=False) -> Session:
		self.config["SESSION_TYPE"] = sess_type
		self.config["SESSION_PERMANENT"] = sess_permanent

		return Session(self)

class SQLAlchemyWrapper:
	def __init__(self, webapp: App):
		self.app = webapp

	def init(self, db_uri: str=None, track_mods: bool=False, **kwargs) -> SQLAlchemy:
		db_uri = db_uri if db_uri else "sqlite:///"+os.path.join(os.getcwd(), "database.db")
		
		self.app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
		self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = track_mods

		self.db = SQLAlchemy(self.app, **kwargs)

		return self.db
		
	def create(self):
		with self.app.app_context():
			self.db.create_all()