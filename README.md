# REST-based Framework for Performability Management of Service Function Chains

### Getting Started

We have designed a platform designed to support, through a dedicated REST interface, the performability management of Service Function Chains. 

Performance aspects (e.g. guarantee an end-to-end delay of an SFC below a given threshold) are modeled through an M/G/k queueing model. 

Availability aspects (e.g. guarantee that the whole SFC has an availability respecting the so-called five nines) are modeled through the formalism of Stochastic Reward Networks (SRN). 

This notwithstanding, the final user is not supposed to know queueing theory or/and SRN since such aspects are automatically managed from software modules embeddded in our framework. The user just needs to pass some parameters in the JSON query as explained in the following.

The output of the framework is an optimal SFC which automatically meets the desired performance (in terms of delay) and availability (in terms of number of nines) constraints.

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

- Automated composition of Service Function Chains 
- Performance evaluation of Service Function Chains
- Availability evaluation of Service Function Chains 
- Can be used to support MANagement and Orchestration (MANO) systems
- Intuitive REST call API

## SFC architecture and nomenclature

In our framework, an SFC is a chain of Virtualized Nodes (VN) where:
- each VN is made of one or more Network Replicas (NR) for redundancy purposes;
- each NR is made of three layer including: Hardware (HW), Hypervisor (HYP), Virtual Network Function (VNF) 

![SFC](https://github.com/mariodim/HASFC/assets/16385982/c375afeb-0561-40d1-91b2-8190fc01f5b1)


## JSON Query format

The JSON Query to be passed to our framework must contain the following parameters:
- NumVN: number of VNs composing the SFC;
- NRmax: max number of NRs constituting each VN;
- VNFmax: max number of VNF on top of each NR;
- MTTF_HW: mean time to failure pertinent to the HW layer;
- MTTF_HYP: mean time to failure pertinent to the HW layer;
- MTTF_VNF: mean time to failure pertinent to the HW layer;
- MTTR_HW: mean time to repair pertinent to the HW layer;
- MTTR_HYP: mean time to repair pertinent to the HW layer;
- MTTR_VNF: mean time to repair pertinent to the HW layer;
- \alpha_k: arrival rate of requests to VN k;
- \beta_k: service rate of VN k;
- D^*: end-to-end delay threshold
- A^*: steady-state availability threshold





