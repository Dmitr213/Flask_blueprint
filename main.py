from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from distance_from_mkad.distance_from_mkad import distance_from_mkad

app = Flask(__name__)

app.register_blueprint(distance_from_mkad, url_prefix='/distance_from_mkad')

menu = [{'url': 'distance_from_mkad', 'title': 'Рассчитать дистанцию от МКАДА'}, ]


@app.route("/")
def index():
    return render_template('index.html', menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
