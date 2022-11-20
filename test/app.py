from flask import Flask

app = Flask(__name__, template_folder="html")
app.debug = True