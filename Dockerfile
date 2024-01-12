FROM python:3.12 as deps
ADD requirements.txt .
RUN pip wheel -r requirements.txt -w /deps
FROM node:20 as frontend
WORKDIR /frontend
ADD package.json .
ADD yarn.lock .
ADD vite.config.js .
ADD code-in-the-dim ./code-in-the-dim
RUN (cd code-in-the-dim && npm ci)
RUN yarn --frozen-lockfile && yarn build
FROM python:3.12
RUN groupadd citadel && useradd -g citadel citadel && mkdir /home/citadel && chown -R citadel:citadel /home/citadel
USER citadel
WORKDIR /home/citadel
COPY --from=deps /deps /deps
ADD requirements.txt /home/citadel
RUN pip install --user --no-cache-dir --find-links=/deps gunicorn -r requirements.txt
ADD . /home/citadel
COPY --from=frontend /frontend/cifront/static/editor /home/citadel/cifront/static/editor
ENV VAR_ROOT /data
ENV PORT 8000
CMD /home/citadel/run-gunicorn.sh
