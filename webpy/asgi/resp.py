from typing import Callable, Awaitable, Union

class Response:
	def __init__(self, send: Callable[[dict], Awaitable]):
		self.send = send
		
	async def start(self, status: int=200, headers: dict[str, str]={"Content-Type": "text/plain"}, trailers: bool=False):
		await self.send(
			{
				"type": "http.response.start",
				"status": status,
				"headers": [
					[name.encode(), value.encode()] for name, value in headers.items()
				],
				"trailers": trailers
			}
		)

	async def senddata(self, body: Union[str, bytes], more_body: bool=False):
		await self.send(
			{
				"type": "http.response.body",
				"body": body if type(body) is bytes else body.encode(),
				"more_body": more_body
			}
		)

		
	async def add_trailers(self, headers: dict[str, str]={"Content-Type": "text/plain"}, more_trailers: bool=False):
		await self.send(
			{
				"type": "http.response.trailers",
				"headers": [
					[name.encode(), value.encode()] for name, value in headers.items()
				],
				"more_trailers": more_trailers
			}
		)