FROM python:3.12.6

RUN mkdir /notes

WORKDIR /notes


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x scripts/*.sh

CMD ["/bin/bash", "/notes/scripts/start.sh"]