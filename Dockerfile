FROM python:3

ADD listener.py /

RUN pip install google_cloud_dns

CMD [ "python", "./listener.py" ]
