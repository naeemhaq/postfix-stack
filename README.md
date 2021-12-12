# AWS Postfix Container Stack

A multi-level AWS cloudformation stacks that deploys infrastructure for postfix MTA container instances in AWS Fargate with: 

- three tier vpc 
- a general security group 
- Internal ALB
- Postfix Container instances
- NLB IP updater stack 

## Cloudformation Stacks: 

### 3tier vpc Stack:
This is [AWS Sample Template](https://github.com/aws-samples/vpc-multi-tier) that will create required VPC and Subnets for the Postfix Fargate instances, internal ALB. [This vpc-multi-tier.yaml](cloudformation-templates/vpc-multi-tier.yaml) stack use all defaults build the network. 

### Sample Security Group
A generic security group that is being used by containers, ALB and lambda functions. At the moment it allows all traffic between the components.  

### Internal ALB
Creates an internal load balancer that will forward requests to the Postfix MTA agent/container instances through an ECS Service.

### Postfix ECS Fargate Instances. 
Creates: 
- ECS cluster
- ECS Taskdefination 
- Fargate container instances 
- ECS Service for the tasks. 

### Starting point Launch Stack
Use [launch-stack.yaml](cloudformation-templates/launch-stack.yaml) to start creating all the nested cloudformation stacks. All the parameters are pre-populated in the launch stack for an environment. 

## Environemnt Variables (pre populated)
ALLOWED_SENDER_DOMAINS=nqtech.ca

# Architecture Diagram

![First Draft image](postfix.drawio.png)