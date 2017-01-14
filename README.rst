Rolodex
=======

Rolodex is a simple app built to demonstrate some basic functionality of
`Lob <https://lob.com/>`_'s API. It stores a virtual "rolodex" of your
associates' addresses, and lets you send them a Christmas card with two clicks.

Well, it won't actually *send* the card, assuming your API key is for Lob's
test environment. But it demonstrates the basic idea: store some addresses
and easily send customizable post cards to them from a web app!

Basics
------

The web app is built with `Flask <http://flask.pocoo.org/docs/0.12/>`_ and a
simple `Angular <https://angularjs.org/>`_ app. Flask renders most of the views
server-side (getting data from Lob's API using your API key), with pagination
for the addresses in the rolodex handled by Angular.

Flask is served by `gunicorn <http://gunicorn.org/>`_ running locally, with
`nginx <https://www.nginx.com/resources/wiki/>`_ proxying HTTP requests to
gunicorn. Static files (including the Angular app and some external Javascript)
are served by nginx.

Obviously there is no authentication or concept of "users" here, so if you
deploy this app somewhere that is publically accessible, anyone with the link
can create/delete addresses or postcards on your Lob account. **Do not deploy
this app publically using an API key for Lob's production environment!** This
is a proof-of-concept meant to demonstrate Lob's functionality, not a
fully-fledged production web app.

Configuration
-------------

You need to specify two configuration values in the ``.backend-env`` file:

1. ``SECRET_KEY`` specifies the key used to sign the session cookie. It doesn't
   really need to be secure, since the session cookie is just used by Flask to
   keep track of failed form submissions (so you don't have to re-enter all the
   information in the case of a failure). Any string will do.
2. ``LOB_API_KEY`` is your Lob account's API key, which you can retrieve from
   the `dashboard <https://dashboard.lob.com/#/settings/keys>`_. I highly
   recommend you only use your test environment key.

Deployment
----------

The app is designed to run with `Docker <https://www.docker.com/>`_. I usually
deploy using `docker-machine <https://docs.docker.com/machine/>`_ and
`docker-compose <https://docs.docker.com/compose/>`_. For example:

- Create a local machine::

    docker-machine create --driver virtualbox rolodex

- Or a `DigitalOcean <https://www.digitalocean.com/>`_ droplet::

    docker-machine create --driver digitalocean --digitalocean-access-token <YOUR DIGITALOCEAN ACCESS TOKEN> rolodex

Then build the app and run it on the machine::

  eval "$(docker-machine env rolodex)"
  docker-compose build
  docker-compose up -d

Future Improvements
-------------------

Although this is just a proof-of-concept, there are some interesting
improvements that could be made to this app::

1. Make it a platform. Add user registration/signin, and scope each set of
   addresses and postcards to a specific user. This requires you to store at a
   minimum the user information and which Lob Address IDs belong to each user.
2. Add address verification. Keep track of whether or not the addresses have
   been verified (they would start off as "unverified") and add a UI flow to
   refine the addresses until they are fully verified using Lob's
   `address verification api <https://lob.com/verification/address>`_. Don't
   allow users to send postcards to unverified addresses.
3. Allow users to customize the postcards that get sent, or upload their own.
4. Keep track of the last time a postcard was sent for a user, and a history of
   previous postcards sent.
