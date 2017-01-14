from flask import (Blueprint, current_app, redirect, url_for, render_template,
                   request, g)
from .errors import InvalidClientInput
from .lob_client import LobClient

api = Blueprint('api', __name__)

@api.before_request
def setup_lob_client():
    g.lob_client = LobClient()

# Views
@api.route('/')
def home():
    return render_template('home.html')

@api.route('/address')
def create_address_view():
    return render_template('create_address.html')

@api.route('/address/<addressId>')
def address(addressId):
    address = g.lob_client.lob.Address.retrieve(addressId)
    return render_template('address.html', address=address)

# Proxy to send/remove so that a single form with multiple submit buttons can
# be used.
@api.route('/address/<addressId>/action', methods=["POST"])
def address_action(addressId):
    data = request.form
    if not data:
        raise InvalidClientInput("form data must be present")

    action = data.get("action")
    if action == 'send':
        return redirect(url_for('.send_postcard_view', addressId=addressId))
    elif action == 'remove':
        g.lob_client.lob.Address.delete(addressId)
        return redirect(url_for('.home'))
    else:
        raise InvalidClientInput("invalid action: %s" % action)

@api.route('/address/<addressId>/remove', methods=["POST"])
def remove_address(addressId):
    address = g.lob_client.lob.Address.retrieve(addressId)
    g.lob_client.lob.Address.delete(address['id'])
    return redirect(url_for('.home'))

@api.route('/address/<addressId>/send')
def send_postcard_view(addressId):
    address = g.lob_client.lob.Address.retrieve(addressId)
    return render_template('send_postcard.html', address=address)

@api.route('/postcard/<postcardId>')
def postcard(postcardId):
    postcard = g.lob_client.lob.Postcard.retrieve(postcardId)
    return render_template('postcard.html', postcard=postcard)

# Form submissions
@api.route('/address', methods=['POST'])
def create_address():
    data = request.form
    if data is None:
        raise InvalidClientInput("form data must be present")

    name = data.get("name")
    if name is not None and len(name) > 50:
        raise InvalidClientInput("name cannot be more than 50 characters")
    company = data.get("company")
    if company is not None and len(company) > 200:
        raise InvalidClientInput("company cannot be more than 200 characters")
    if not name and not company:
        raise InvalidClientInput("name or company must be specified")

    address_line1 = data.get("addressLine1")
    if not address_line1:
        raise InvalidClientInput("first line of address must be specified")
    if len(address_line1) > 200:
        raise InvalidClientInput("address line cannot be more than 200 "
                                 "characters")
    address_line2 = data.get("addressLine2")
    if address_line2 and len(address_line2) > 200:
        raise InvalidClientInput("address line cannot be more than 200 "
                                 "characters")

    address_country = data.get("country")
    address_city = data.get("city")
    if address_city and len(address_city) > 200:
        raise InvalidClientInput("city cannot be more than 200 characters")
    address_state = data.get("state")
    if address_state and len(address_state) > 200:
        raise InvalidClientInput("state cannot be more than 200 characters")
    address_zip = data.get("zip")
    if address_zip and len(address_zip) > 40:
        raise InvalidClientInput("zip cannot be more than 40 characters")

    if address_country == 'US':
        if not address_city:
            raise InvalidClientInput("city must be specified for US")
        if not address_state:
            raise InvalidClientInput("state must be specified for US")
        if not address_zip:
            raise InvalidClientInput("zip must be specified for US")
    else:
        address_state = None # If state was specified but country is not US,
                             # null it out

    phone = data.get("phone")
    if phone and len("phone") > 40:
        raise InvalidClientInput("phone cannot be more than 40 characters")
    email = data.get("email")
    if email and len("email") > 40:
        raise InvalidClientInput("email cannot be more than 40 characters")

    address = g.lob_client.lob.Address.create(
            name=name,
            company=company,
            email=email,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            address_city=address_city,
            address_state=address_state,
            address_zip=address_zip,
            address_country=address_country
    )
    return redirect(url_for('.address', addressId=address["id"]))

@api.route('/address/<addressId>/send', methods=['POST'])
def send_postcard(addressId):
    data = request.form
    if data is None:
        raise InvalidClientInput("form data must be present")

    address = g.lob_client.lob.Address.retrieve(addressId)
 
    message = data.get("message")
    if message is None:
        raise InvalidClientInput("a message must be specified")
    if len(message) > 350:
        raise InvalidClientInput("message must be less than 350 characters")

    postcard = g.lob_client.lob.Postcard.create(
            to_address=address["id"],
            front=current_app.config["CHRISTMAS_CARD_TEMPLATE"],
            message=message
    )
    return redirect(url_for('.postcard', postcardId=postcard["id"]))
