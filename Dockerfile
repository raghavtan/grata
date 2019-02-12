FROM python:3.6

# Install KubeCTL
RUN apt-get update -q && apt-get install -y apt-transport-https -q
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list
RUN apt-get update -q
RUN apt-get install -y kubectl libedit-dev build-essential gcc -q

WORKDIR /usr

RUN mkdir /usr/app

WORKDIR /usr

COPY . /usr/app

WORKDIR /usr/app

RUN pip install -r requirements.txt
#
#ENTRYPOINT ["pipenv"]

EXPOSE 8001

CMD ["python" ,"main.py"]