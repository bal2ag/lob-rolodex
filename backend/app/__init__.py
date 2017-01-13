from flask import Flask, jsonify, render_template

def create_app():
    from config import Config
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    import logging, sys
    date_fmt = "%Y-%m-%dT%H:%M:%SZ"
    fmt_string = "APP_[%(levelname)s %(asctime)s %(process)d " +\
        "%(threadName)s %(filename)s:%(lineno)d] %(message)s"
    formatter = logging.Formatter(fmt_string, date_fmt)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel("DEBUG")

    from errors import BaseError
    @app.errorhandler(BaseError)
    def handle_error(error):
        return render_template('error.html', status=error.status_code,
                message=error.message)

    from api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from ajax import api as ajax_blueprint
    app.register_blueprint(ajax_blueprint, url_prefix='/ajax')

    from healthcheck import healthcheck as healthcheck_blueprint
    app.register_blueprint(healthcheck_blueprint)

    return app
