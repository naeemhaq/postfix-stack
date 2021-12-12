# AWS Postfix Container Stack

AWS cloudformation stack that deploys postfix MTA container instances in AWS Fargate with: 

- three tier vpc 
- a general security group 
- Internal ALB
- Postfix Container instances
- NLB IP updater stack 

## Cloudformation Stacks: 

### 3tier vpc Stack:
This will create required VPC and Subnets required for the Postfix Fargate instances, internal ALB and helper lambda functions for the target group updater and log groups. I have used [this vpc-multi-tier.yaml](cloudformation-templates/vpc-multi-tier.yaml) file to build the network. 

### Sample Security Group
A generic security group that is being used by containers, ALB and lambda functions. 

### ECS Instances and ALBs
Use [launch-stack.yaml](cloudformation-templates/launch-stack.yaml) to start creating the nested cloudformation stacks. All the parameters are pre-populated in the launch stack for an environment. 

### NLB IP Updater (Util)
A utility stack that updates the target group if in case a public ALB is created to access the postfix stack from another/edge network. 

## Environemnt Variables
ALLOWED_SENDER_DOMAINS=nqtech.ca

# Architecture Diagram

![First Draft image](postfix.drawio.png)