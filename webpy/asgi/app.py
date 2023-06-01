from typing import Callable, Awaitable
from .resp import Response
from .http_request import Request, HTTP_METHODS

class App:
	def __init__(self):
		self._map = {} # typehint this

	def route(self, path: str, methods: list[str]=["GET"]):
		def wrapper(func: Callable[[Request, Response], Awaitable[None]]):
			self._map[path] = {
				"func": func,
				"methods": methods
			}
			
			return func
		return wrapper
	
	async def _page_not_found(self, request: Request, responsectx: Response):
		await responsectx.start(status=404)
		await responsectx.senddata("Error 404 - Page not Found!")

		print(f"Error 404 - page not found <{request.path} {request.method}>")
	
	async def _invalid_method(self, request: Request, responsectx: Response):
		pass # code this up

	async def _handle_request(self, scope: dict[str], receive: Callable[[], Awaitable[dict[str]]], send: Callable[[dict], Awaitable[None]]):
		request = Request(receive, scope)
		response = Response(send)

		data = self._map.get(
			request.path,
			{
				"func": self._page_not_found,
				"methods": HTTP_METHODS
			}
		)

		if request.method not in data["methods"]:
			await self._invalid_method(request, response)
			return
		
		await data["func"](request, response)

	async def __call__(self, scope: dict[str], receive: Callable[[], Awaitable[dict[str]]], send: Callable[[dict], Awaitable[None]]):
		await self._handle_request(scope, receive, send)