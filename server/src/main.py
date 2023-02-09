from flask import Flask

from api import blueprint as api_blueprint

app = application = Flask(__name__)
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
