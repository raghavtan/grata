FROM python:3.6

# Install KubeCTL
RUN apt-get update && apt-get install -y apt-transport-https
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list
RUN apt-get update
RUN apt-get install -y kubectl

WORKDIR /usr

RUN mkdir /usr/app

WORKDIR /usr

COPY . /usr/app

RUN pip3 install pipenv

WORKDIR /usr/app

RUN pipenv install
#
#ENTRYPOINT ["pipenv"]

EXPOSE 8001

CMD ["pipenv","run", "python" ,"main.py"]