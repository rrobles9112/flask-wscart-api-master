FROM python:3.9-slim-buster
COPY . /web
VOLUME [ "/web/app" ]
WORKDIR /web
RUN pip install virtualenv
RUN virtualenv -p python3 venv
RUN pip install autoenv
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["run.py"]
