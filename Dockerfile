FROM python:3.6

WORKDIR /usr

RUN mkdir /usr/app

WORKDIR /usr

COPY . /usr/app

RUN pip3 install pipenv

WORKDIR /usr/app

RUN pip3 install -r requirements.txt

EXPOSE 8001

CMD ["python" ,"main.py"]
