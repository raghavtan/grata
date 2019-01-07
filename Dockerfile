FROM python:3.6.4

WORKDIR /usr

RUN mkdir /usr/app

WORKDIR /usr

COPY . /usr/app

RUN pip3 install pipenv

WORKDIR /usr/app

RUN pipenv install --deploy --system

ENTRYPOINT ["pipenv"]

EXPOSE 8001

CMD ["run", "python" ,"main.py"]
