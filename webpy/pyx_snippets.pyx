from .pysite_semantic_tags import *

def theme(data: str=None, children: list=None, name: str=""):
	theme_css = f"https://user0332.github.io/webpy/themes/{name}.css"
	theme_js = f"https://user0332.github.io/webpy/themes/{name}.js"

	return (
		<pyx>
			<link rel="stylesheet" href={theme_css}></link>
			<script src={theme_js} defer></script>
		</pyx>
	)