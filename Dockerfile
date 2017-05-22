FROM python:3.6
RUN groupadd citadel && useradd -g citadel citadel && mkdir /home/citadel && chown -R citadel:citadel /home/citadel
USER citadel
WORKDIR /home/citadel
RUN pip install --user gunicorn && rm -r /home/citadel/.cache
ADD requirements.txt /home/citadel
RUN pip install --user -r requirements.txt && rm -r /home/citadel/.cache
ADD . /home/citadel
ENV VAR_ROOT /data
ENV PORT 8000
CMD /home/citadel/run-gunicorn.sh
