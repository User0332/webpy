from dataclasses import dataclass

@dataclass
class Client:
	host: str
	port: int

class Server:
	def __init__(self, server):
		if server[1]:
			self.host: str = server[0]
			self.port: int = server[1]
			self.is_unix_socket = False
		else:
			self.path: str = server[0]
			self.is_unix_socket = True