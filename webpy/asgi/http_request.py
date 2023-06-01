import json
from flask import request
from multidict import MultiDict, CIMultiDict
from typing import Union, Callable, Awaitable, Generator
from .misc_classes import Client, Server

HTTP_METHODS = ["GET", "POST", "DELETE", "HEAD", "PUT", "CONNECT", "OPTIONS", "TRACE", "PATCH"]

class Request:
	def __init__(self, recieve: Callable[[], Awaitable[dict[str]]], scope: dict[str]) -> None:
		self.path: str = scope["path"]
		self.method: str = scope["method"]
		self.query_string: str = scope["query_string"].decode()
		self.query_params: MultiDict[str, str] = MultiDict(
			(decl.split('=')[0], decl.split('=')[1]) for decl in self.query_string.split('&') if decl
		)
		self.form = self.query_params
		self.headers: CIMultiDict[str, str] = CIMultiDict(
			(name.decode(), value.decode()) for (name, value) in scope["headers"]
		)

		try: self.client = Client(*scope["client"])
		except TypeError: self.client = None

		try:
			self.server = Server(scope["server"])
			self.url: str = f"http://{self.server.host}:{self.server.port}{self.path}?{self.query_string}"
		except TypeError: self.server = None

		self._complete_body = b""

		self._recieve = recieve

	@property
	async def content(self):
		try: return (await self.body).decode()
		except UnicodeDecodeError: return None

	@property
	async def json(self) -> Union[dict, None]:
		try: return json.loads(await self.body)
		except json.decoder.JSONDecodeError: return None

	@property
	async def body(self) -> bytes:
		if not self._complete_body:
			more_body = True

			while more_body:
				req = await self._recieve()

				assert req["type"] == "http.request"

				self._complete_body+=req["body"]
				more_body = req["more_body"]

		return self._complete_body
	
	@property
	async def stream(self) -> Generator[tuple[bytes, bytes], None, None]:
		more_body = True

		while more_body:
			req = await self._recieve()

			if req["type"] == "http.disconnect": break

			if req["type"] == "http.request":
				self._complete_body+=req["body"]
				yield [req["body"], self._complete_body]

				more_body = req["more_body"]
