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

### Prerequisites

Things you need to install the application and how to install them
- python>=3.6
- pip
- pipenv

```
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
