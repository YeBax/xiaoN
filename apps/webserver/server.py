from webserver.views import app


def run():
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
