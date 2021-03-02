# High Availability Service Function Chain (HASFC)

### Getting Started

HASFC is a platform designed to support, through a dedicated REST interface, the MANagement and Orchestration (MANO) infrastructure in deploying SFCs with an optimal availability/cost trade off.

## Prerequisites
```sh
- Windows-based or Linux-based platforms 
- TimeNET (https://timenet.tu-ilmenau.de) freely available for non-commercial purposes
- Python (>= )
```


## Features

- Automated stochastic modeling of virtualized nodes (three-layered)
- Automated composition of Service Function Chains 
- Availability evaluation of Service Function Chains 
- Can be used also as a stand-alone framework without the MANO
- Intuitive REST call API

## The Algorithm 

HASFC relies on a designed-from-scratch algorithm (named HASFCBuilder) which is equipped with: i) an availability model builder aimed to construct probabilistic models of the SFC nodes in terms of failure/repair actions; ii) a chaining and selection module to compose the possible redundant SFCs, and extract the best candidates thereof. 
Take a look to our Python code available here: XXX

## Running the Tests

Testing the functionalities of HASFC and HASFCBuilder is quite easy. A simple REST client (e.g. Insomnia) can be freely downloaded to test the whole environment. 
