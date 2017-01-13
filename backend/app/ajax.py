from flask import (Blueprint, Response, g, request, jsonify, current_app)

from .errors import BaseError
from .lob_client import LobClient

api = Blueprint('ajax', __name__)

@api.before_request
def setup_lob_client():
    g.lob_client = LobClient()

@api.route('/addresses')
def paginate_addresses():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    addresses = ajax_wrap(g.lob_client.lob.Address.list,
            limit=limit,
            offset=((page - 1) * limit),
            include=['total_count'])
    if isinstance(addresses, Response):
        return addresses # Error occurred
    
    return jsonify({
        "addresses": addresses["data"],
        "total": addresses["total_count"]
    })

def ajax_wrap(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except BaseError as e:
        response = jsonify(e.serialize())
        response.status_code = e.status_code
        return response
