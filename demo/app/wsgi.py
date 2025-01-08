
import requests
from flask import Flask, Response, abort, send_file, jsonify
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/health")
@metrics.do_not_track()
def health():
    return Response("", status=204)


@app.route("/large-file")
def large_file():
    return send_file(
        "large_file.json", 
        mimetype="text/json", 
        download_name="large_file.json",
    )


@app.route("/github-users/<username>")
def github_users(username):
    response = requests.get(f"https://api.github.com/users/{username}", timeout=3)
    if response.status_code != 200:
        abort(response.status_code)

    user = response.json()
    return jsonify(data=user)


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
