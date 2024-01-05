# Citadel

A **C**ode **I**n **T**he D**a**rk event management system.

Citadel is an integrated Django app for managing [Code In The Dark][citd] events.

## Getting started

### Using Docker

This will assume you want to store variable data
(database, assets, screenshots, etc.)
in the "data" subdirectory of the current directory.

You will be prompted for admin user credentials
during the first step.

Naturally, replace `FIGUREOUTSOMETHINGSECRET`.

```bash
docker build -t citadel .
mkdir `pwd`/data
# first run:
docker run -it \
    -e SECRET_KEY=FIGUREOUTSOMETHINGSECRET \
    -v `pwd`/data:/data \
    citadel \
    ./initialize.sh
# start the server, publishing on port 8000
docker run -it \
    -e SECRET_KEY=FIGUREOUTSOMETHINGSECRET \
    -v `pwd`/data:/data \
    -p 8000:8000 \
    citadel
```

### Other deployment systems

Citadel is a plain ol' Django project configured with
environment variables, as is best practice these days,
so you should have no problems getting it up and running
under uWSGI/Gunicorn/what-have-you.

The environment variables are:

- `DEBUG`: Whether Django's DEBUG mode is on.
- `SECRET_KEY`: The Django secret key. Make it yours.
- `VAR_ROOT`: Where to store all sorts of variable data (static/media/SQLite database). Defaults to `var` in the project root.
- `DATABASE_URL`: An URL pointing to your database. Defaults to an SQLite database under `var`.

So,

```bash
pip install uwsgi
uwsgi --master --virtualenv $VIRTUAL_ENV --http :8000 -p5 --env DEBUG=false --env SECRET_KEY=asdf --wsgi=citadel.wsgi
```

should get you up and running if you're averse to containers.

## Development

- Get a Python 3.x virtualenv up and running
- Set the `DEBUG` environment variable to something truthy
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py runserver`
- To edit the, erm, editor, `npm run dev` in another tab for Webpack in watch mode.

## License

- The project is Copyright (c) 2017, Valohai; licensed under the MIT License.
- The Code in the Dark name and logos are Copyright (c) 2017, Tictail Inc.;
  licensed under the 3-clause BSD License (see `LICENSE.tictail`).
  The use of the Code in the Dark brand in this repository is in good faith.
  Any requests for external use should seek the permission of Tictail directly.
- `cifront/app` and `cifront/templates/editor.html`
  are adapted from the [Code in the Dark Editor][citdedit],
  which is Copyright (c) 2015, Tictail Inc.;
  licensed under the 3-clause BSD License (see `LICENSE.tictail`).

[citd]: http://codeinthedark.com/
[citdedit]: https://github.com/codeinthedark/editor
