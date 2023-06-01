from dataclasses import dataclass

@dataclass
class Rule:
	path: str
	methods: list[str]
	...