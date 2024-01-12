FROM python:3.12 as deps
ADD pyproject.toml .
RUN pip wheel . -w /deps
FROM node:20 as frontend
WORKDIR /frontend
ADD package.json .
ADD package-lock.json .
ADD vite.config.js .
ADD code-in-the-dim ./code-in-the-dim
RUN (cd code-in-the-dim && npm ci)
RUN npm ci && npm run build
FROM python:3.12
RUN groupadd citadel && useradd -g citadel citadel && mkdir /home/citadel && chown -R citadel:citadel /home/citadel
USER citadel
WORKDIR /home/citadel
COPY --from=deps /deps /deps
ADD pyproject.toml /home/citadel
RUN pip install --user --no-cache-dir --find-links=/deps gunicorn -e .
ADD . /home/citadel
COPY --from=frontend /frontend/cifront/static/editor /home/citadel/cifront/static/editor
ENV VAR_ROOT /data
ENV PORT 8000
ENV SERVE_MEDIA 1
CMD /home/citadel/run-gunicorn.sh
