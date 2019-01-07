FROM kennethreitz/pipenv

WORKDIR /usr

RUN mkdir /usr/app

WORKDIR /usr

COPY . /usr/app

RUN pip install pipenv

WORKDIR /usr/app

RUN pipenv install .

ENTRYPOINT ["pipenv"]

EXPOSE 8001

CMD ["run", "python" ,"main.py"]
