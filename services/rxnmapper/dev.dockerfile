FROM continuumio/miniconda3:4.8.2   AS rxnmapper

# set env variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1


COPY requirements_pip.txt /tmp/requirements_pip.txt

# install dependencies
RUN pip install --trusted-host=files.pythonhosted.org --trusted-host=pypi.python.org  \
    --trusted-host=pypi.org --trusted-host=pypi.python.org -r /tmp/requirements_pip.txt && \
    rm /tmp/*

## in the future we might need to install rxnmapper via gilab, rather than pip
#WORDKDIR /tmp/ \
#RUN git clone https://github.com/rxn4chemistry/rxnmapper

COPY src /code/src
WORKDIR /code/src







