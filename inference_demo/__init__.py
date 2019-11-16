from inference_demo.version import __version__

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


from inference_demo.load_binaries import load_binaries

tf_binaries, dict_binaries = load_binaries(app)

from inference_demo import views
