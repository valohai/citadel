# Citadel

A **C**ode **I**n **T**he D**a**rk event management system.

Citadel is an integrated Django app for managing [Code In The Dark][citd] events.

## Deployment

### Using Docker

This will assume you want to store variable data
(database, assets, screenshots, etc.)
in the "data" subdirectory of the current directory.

The default admin password is `totoro` (unless you set
one with the `ADMIN_PASSWORD` environment variable).

Naturally, replace `FIGUREOUTSOMETHINGSECRET` with
an uniquely generated secret key.

```bash
docker build -t citadel .
mkdir `pwd`/data
# start the server, publishing on port 8000
docker run -it \
    -e SECRET_KEY=FIGUREOUTSOMETHINGSECRET \
    -v `pwd`/data:/data \
    -p 8000:8000 \
    citadel
```

## Development without Docker

- Ensure you've cloned submodules (`git submodule update --init --recursive`)
- Install dependencies for the editor (`npm ci` in `code-in-the-dim/`)
- Get a Python 3.11+ virtualenv up and running
- Run `pip install -e .[dev]`
- Set the `DEBUG` environment variable to something truthy
- Run `npm ci` and `npm run build` (with `--watch` if you need to)
- `python manage.py migrate`
- `python manage.py cicore_init`
- `python manage.py runserver`

## License

- The project is Copyright (c) 2017, Valohai; licensed under the MIT License.
- The Code in the Dark name and logos are Copyright (c) 2017, Tictail Inc.;
  licensed under the 3-clause BSD License (see `LICENSE.tictail`).
  The use of the Code in the Dark brand in this repository is in good faith.
  Any requests for external use should seek the permission of Tictail directly.

[citd]: http://codeinthedark.com/
[citdedit]: https://github.com/codeinthedark/editor
