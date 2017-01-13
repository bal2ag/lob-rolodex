from flask import Blueprint

healthcheck = Blueprint('healthcheck', __name__)

@healthcheck.route("/health_check", methods=["GET"])
def health_check():
    return "Healthy!"
