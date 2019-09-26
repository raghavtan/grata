# Grata 

![Alt text](docs/logo.gif?raw=true "grata")

[![Build Status](https://travis-ci.com/raghavtan/grata.svg?branch=master)](https://travis-ci.com/raghavtan/grata)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Requires.io](https://img.shields.io/requires/:service/:user/:repo.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/badges/shields.svg)


Lightweight Fast api framework
- Also can be used as a sustainable microservice build framework

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Direcorty Structure
```
├── CHANGES.txt
├── Dockerfile
├── Jenkinsfile
├── LICENSE
├── MANIFEST.in
├── Pipfile
├── README.md
├── __init__.py
├── benchmark.MD
├── compile.py
├── config
│   ├── __init__.py
│   ├── email_template.html.j2
│   ├── kube-prod.yaml
│   └── logging.cfg
├── config.json
├── decorators
│   └── __init__.py
├── docs
│   └── logo.gif
├── k8s
│   └── config.json
├── main.py
├── requirements.txt
├── setup.py
├── src
│   ├── __init__.py
│   ├── cache_engine.py                # Cache engine for web server (can be used whle defining cache=True in routes.py) 
│   ├── handlers
│   │   ├── __init__.py
│   │   ├── alerts.py
│   │   ├── base.py
│   │   ├── helper.py
│   │   ├── incoming.py                 # Handler for incoming alerts hooks(creates alert job background task)
│   │   ├── reporting.py                # Handler to trigger background job for reports (creates reporting job task)
│   ├── internal_handlers.py
│   ├── internals
│   │   ├── __init__.py
│   │   └── notification_utils
│   │       ├── __init__.py
│   │       └── source_manager.py       # Incoming Alerts source parser
│   ├── jobs
│   │   ├── __init__.py
│   │   ├── alert_job.py                # Alert Notification Job backgrond task (triggered for every handler hit)
│   │   └── reporting_job.py            # Report generation background job (triggered for every handler hit)
│   ├── listeners
│   │   ├── __init__.py
│   │   ├── elastic.py                  # ES connection pool maintainer 
│   │   ├── internal_statistics.py
│   │   ├── job_scheduler.py            # Job scheduler metacl
│   │   ├── kafka_client.py
│   │   ├── kafka_client2.py
│   │   ├── kafka_consumer.py
│   │   ├── kubernetes_client.py
│   │   ├── log_factory.py
│   │   └── slack_client.py              # Slack Client 
│   ├── resources
│   │   ├── __init__.py
│   │   ├── ansible_mail.py              # send mail wrapper
│   │   ├── kubectl.py
│   │   ├── rds
│   │   │   ├── __init__.py
│   │   │   ├── mysql_parser.py          # RDS logs fetch from AWS and parsing (uses rds.py underneth)
│   │   │   └── rds.py                   # RDS logs parsing engine (low-level client)
│   │   └── reports.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── routes.py                    # Routes defination factory 
│   ├── routes_loader.py                 # Parses routes.py to load into application 
│   └── server.py                        # Web server base class
├── tox.ini
└── utilities
    ├── __init__.py
    ├── log_factory.py
    ├── os_level.py
    ├── scheduler.py
    └── termination_protection.py
```

### Prerequisites

Things you need to install the application and how to install them
- python>=3.6
- pip
- pipenv

```
GCC
C++ Devel package
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install pipenv
```

### Installing

Installing application 

```
git clone https://github.com/raghavtan/grata
cd grata
```
Install with virtualenv
```
pipenv install --deploy
```
System Install
```
python main.py install
```
Docker 
```$xslt
docker build . -t grata
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

```$xslt
cd grata
pipenv run python setup.py test
```

### Linting tests

Explain what these tests test and why

```
pipenv run python setup.py lint
```

## Deployment
System deployment 
```$xslt
pipenv run python main.py run
```
Docker deployment
```$xslt
docker run  -d grata
```
## Built With


## Contributing

```$xslt
cd grata
pipenv install --deploy
pipenv shell
```
- Install packages with ```pipenv install {PACKAGE_NAME}```
- Start making changes to code but before commiting changes do ```pipenv update```
- And also run lint before commiting changes ```pipenv run python setup.py lint```
```$xslt
pipenv 
```

## Versioning


## Authors


## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
