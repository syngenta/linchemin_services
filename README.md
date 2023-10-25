[![Powered by RDKit](https://img.shields.io/badge/Powered%20by-RDKit-3838ff.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAFVBMVEXc3NwUFP8UPP9kZP+MjP+0tP////9ZXZotAAAAAXRSTlMAQObYZgAAAAFiS0dEBmFmuH0AAAAHdElNRQfmAwsPGi+MyC9RAAAAQElEQVQI12NgQABGQUEBMENISUkRLKBsbGwEEhIyBgJFsICLC0iIUdnExcUZwnANQWfApKCK4doRBsKtQFgKAQC5Ww1JEHSEkAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wMy0xMVQxNToyNjo0NyswMDowMDzr2J4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDMtMTFUMTU6MjY6NDcrMDA6MDBNtmAiAAAAAElFTkSuQmCC)](https://www.rdkit.org/)  
[![Powered by FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-green)](https://fastapi.tiangolo.com/)
[![Aligned with OpenAPI](https://img.shields.io/badge/Aligned%20with-OpenAPI-green)](https://www.openapis.org/)    
[![Powered by Docker](https://img.shields.io/badge/Powered%20by-Docker-Blue)](https://www.docker.com/)    
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)   
[![Contributions](https://img.shields.io/badge/contributions-welcome-blue)](https://github.com/syngenta/linchemin/blob/main/CONTRIBUTING.md)

# LiChemIn_Services
LinChemIn_Services is a collection of services that act as companions of the LinChemIn package.    
Some LinChemIn workflows depend on tools are proprietary, and require separate license incompatible with LinChemIn MIT license; 
other tools are not distributed as python libraries, or the python library include complex dependencies, that might create conflicts with LinChemIn itself or other packages.     
In such case we prefer to wrap the tool into a container and expose its functionalities via a REST API, letting LinChemIn satisfy its dependencies via an SDK.
We use the FastAPI framework because it natively provides an openAPI documentation page, simplifying the alignment of documentation to code.  
We also provide a simple SDK that operates the endpoints of each service API. 
This SDK is an installable package, and would simplify the usage of the services from python code.
The SDK is also used to perform end-to-end tests on each service. This ensures all the activated services are up and running and that they are behaving as expected.
The test set provide also good usage examples: the SDK contains a Service.EndPoint architecture, and for each endpoint input/output examples are part of the pydantic schemas. 

## Using the services 
To use the services it is necessary to fire up the individual servers, so that the REST endpoints are available at the specified address.    
We describe below two ways of doing it on a laptop, using simple tools like [docker] (https://www.docker.com/). This leads to a deployment that is good for experimenting and development, but unsuitable for production purposes.  
In our company we use a professional deployment to expose such functionalities: what you see here is a strongly stripped down version of the services we regularly use.   
The purpose is to provide the user with a bare minimum of functionalities to reproduce the complex workflows that involve LinChemIn.  
The user can take these services we provide as an inspiration to build professional microservices, deployed at scale in the preferred environment, rather than with docker on a laptop, as described here.  
Of curse, in such case, it is necessary to provide to the SDK functions the correct base url.   
The code of each service contains detailed information about required input/output of each endpoint, to ensure compatibility with the LinChemIn workflows. 

### docker [preferred]
This repository provides a set of docker files to construct the necessary containers and to fire up the included services. 
A global docker-compose.yml file in the /services directory would set up all services at once.
Optionally, the user can process only selected services (see docker compose user manual)
This command creates the containers, starts the services, and assigns to each a dedicated port, accessible from the outside of the container.

> cd /services/  
> docker compose build  
> docker compose up

Alternatively, the user can enter each service directory and create a container for the relative service.
This might be useful in development as the source is mounted in the container, to allow live observation of code changes.
The uvicorn server restarts automatically at each modification of the code.

### virtual environment 
If the user does not want to use docker, it is possible to create a virtual environment for each service, installing in each the necessary dependencies.  
On separate shells, the user can start up an uvicorn server, taking care of the port number.  

## Available services  

### rxnmapper_service [![Powered by rxnmapper](https://img.shields.io/badge/Powered%20by-rxnmapper-blue)](http://rxnmapper.ai/)  
The IBM team developed a chemically agnostic attention-guided reaction mapper (rxnmapper) based on a textual representation of chemical reactions. 
This reaction atom-to-atom mapper is thus based on a model constructed with Natural Language Processing (NLP) techologies.
That is definitely a novel approach to reaction atom-to-atom mapping that works surprisingly well.   
We encourage the reader to visit the dedicated [page](http://rxnmapper.ai/) and read the associated [publication](https://www.science.org/doi/10.1126/sciadv.abe4166).
The source code of the tool is available in [github](https://github.com/rxn4chemistry/rxnmapper) as well as a python package available in [pypi](https://pypi.org/project/rxnmapper/) and easily installable via pip 
The tool includes a trained model, developed by the authors in 2020 using USPTO [data](https://ibm.ent.box.com/v/RXNMapperData) and the code to perform predictions. 
To this aim, rxnmapper depends on (and installs) the transformers and torch packages, among others. 
These packages (and their dependencies) might conflict with the requirements of other packages/libraries LinChemIn depends on.
For this reason we decided to depend on namerxn indirectly via an API-SDK channel, rather than creating direct dependency on the installable python package.  
  
The service exposes two endpoints:  
* /metadata     : containing information about the software used, in this case the version of RDKit and that of rxnmapper  
* /run_batch    : receiving list of queries and processing them in batch  

The openAPI doc page  provides both examples and documentation   
[http://127.0.0.1:8003/docs#](http://127.0.0.1:8003/docs#)

## Testing the services
The tests directory includes simple end-to-end tests aimed at checking that the services are up and running and that 
the actual response of the single endpoints match the expected one.  
The unit tests for the single services in contained inside each service's directory.  
After installation and before running the tests, it is necessary to configure the package. This will create the user_home/linchemin_services directory containing a .settings.yaml file with some default parameters and a .secrets.yaml storing keys for secrets.  

> pip install -e .[dev]  
> linchemin_services_configure  
> cd tests    
> pytest  

