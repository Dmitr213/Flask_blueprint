from flask import Flask, render_template
from distance_from_mkad.controllers import module

app = Flask(__name__)

app.register_blueprint(module, url_prefix='/distance_from_mkad')

app.secret_key = 'secret key'

menu = [{'url': 'distance_from_mkad', 'title': 'Рассчитать дистанцию от МКАД'}, ]


@app.route("/")
def index():
    return render_template('index.html', menu=menu)


if __name__ == "__main__":
    app.run(debug=False)
