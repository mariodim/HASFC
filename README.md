# High Availability Service Function Chain (HASFC)

### Getting Started

HASFC is a platform designed to support, through a dedicated REST interface, the MANagement and Orchestration (MANO) infrastructure in deploying SFCs with an optimal availability/cost trade off. 

## Prerequisites
```sh
- Windows-based (actually tested on Win10) or Linux-based platforms 
- TimeNET 4.5 or higher (https://timenet.tu-ilmenau.de) freely available for non-commercial purposes
- Python 3.6 or higher
```
## Setup
For Win users: add the file SOLVE.bat in the folder 
```sh
C:\Program Files (x86)\TimeNET\TimeNET\EDSPN\StatAnalysis\scripts
```
To automatically setup all the needed Python libraries run the following command:
```sh
pip install -r requirements.txt
```
Start the REST application through the following command:
```sh
python app.py
```

## Features

- Automated stochastic modeling of virtualized nodes (three-layered)
- Automated composition of Service Function Chains 
- Availability evaluation of Service Function Chains 
- Can be used also as a stand-alone framework without the MANO
- Intuitive REST call API

## The Algorithm 

HASFC relies on a designed-from-scratch algorithm (named HASFCBuilder) which is equipped with: i) an availability model builder aimed to construct probabilistic models of the SFC nodes in terms of failure/repair actions; ii) a chaining and selection module to compose the possible redundant SFCs, and extract the best candidates thereof. 

## Running the Tests

Testing the functionalities of HASFC and HASFCBuilder is quite easy. A simple REST client (e.g. Postman or Insomnia) can be freely downloaded to test the whole environment. We have prepared two sample requests:
- POST: it contains all the parameters to perform a complete query to the HASFC. (See the file example_post). Note: the IP address 127.0.0.1 must be replaced with the IP address where HASFC is running.
- GET:  it contains the simplest query to the HASFC (parameters: availability target and number of max SFCs to visualize). (See the file example_get). Note: the IP address 127.0.0.1 must be replaced with the IP address where HASFC is running.
