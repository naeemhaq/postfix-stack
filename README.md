# AWS GSC GSIP

AWS Account: landmass-lcnp-dev

## Manual Steps:
Created Edge-vpc security group  because it did not exist before. 

### Route 53:
Created two hosted zones:

1. ldrs.geoconnex.ca (Gabriel is working with the registrar to point NS records correctly. We tried but we were not successful)

2. Created a temp hosted zone gsip-dev.geo.ca to test my initial Cloudforamtion stacks. At the moment the NS records are pointed to FGP-Common Route 53 record which will be deleted once the official zone is fixed. 

### ACMs  
Two ACMs for public and private load balancers created which are being used by the CF stacks. 

### ECS repository and docker images  

Created two repos: 
1. GSIP
2. Inferencer and pushed images from my linux dev box which is in the FGP-Dev account. 

### Deployment Bucket 
s3://geoconnex-deployment-bucket/cloudformation-templates/3-tier-vpc.yml

### RDF Data files bucket 
s3://geoconnex-data-dev/rdf/

### Create Neptune DB manually
Before deploying neptune db following things need to be done ( there is a task in Jira to automate this)

- Create S3 bucket 
- create vpc endpoint for s3 to be used by neptune
- Create IAM role 
- create Neptune DB 
- Attach IAM role to NeptuneDB 

[Article where all is explained](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-IAM.html#bulk-load-tutorial-IAM-add-role-cluster)

### Source Code: 
All the source code for the cloudformation stack is https://gccode.ssc-spc.gc.ca/gccp/aws-gsc-gsip

## Cloudformation Stacks: 

### 3tier vpc Stack:
This is the normal 3 tier vpc stack that we run in every new account. I have used [this 3-tier-vpc.yml](cloudformation-templates/3-tier-vpc.yml) file to build the network. 

You can check out the stack created in the aws account. 
### ECS Instances and ALBs
Use [launch-stack.yaml](cloudformation-templates/launch-stack.yaml) to start creating the nested cloudformation stacks. All the parameters are pre-populated in the launch stack for this environment. 

There is one stack already running in the landmass-lcnp-dev account. 


## Neptune Database
From a cloud9 devbox that I created in the landmass-lcnp-dev account I can access below neptune database. If anyone wants to create there own cloud9 dev environment make sure to create rules for the security groups. 

curl -v https:\\geoconnex-dev-instance-1.cadlcqyheg76.ca-central-1.neptune.amazonaws.com:8182/status

curl -v https:\\geoconnex-dev-instance-1.cadlcqyheg76.ca-central-1.neptune.amazonaws.com:8182/sparql 

### Setup RF4J Console to connect to Neptune by running below shell commands: 
```
sudo /usr/sbin/amazon-linux-https enable
sudo yum clean expire-cache
sudo yum clean all
sudo yum -y update
sudo yum install java-1.8.0-devel
sudo /usr/sbin/alternatives --config java
```
Setup up access keys to download RD4J zip file from S3 bucket
```
export AWS_ACCESS_KEY_ID="AS****
aws s3 cp s3://geoconnex-data-dev/eclipse-rdf4j-3.7.4-sdk.zip .
unzip -d rd4j eclipse-rdf4j-3.7.4-sdk.zip 
```
RD4J Console prompt and sample output: 
```
AWSReservedSSO_PowerUser_df1f39ec70d01410:~/environment $ rd4j/eclipse-rdf4j-3.7.4/bin/console.sh 
13:42:52.421 [main] DEBUG org.eclipse.rdf4j.common.platform.PlatformFactory - os.name = linux
13:42:52.438 [main] DEBUG org.eclipse.rdf4j.common.platform.PlatformFactory - Detected Posix platform
Connected to default data directory
RDF4J Console 3.7.4
Working dir: /home/ec2-user/environment
Type 'help' for help.
> open neptune
Opened repository 'neptune'
```
For more information on the RDF4J console [see this link](https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-sparql-rdf4j-console.html) 

Once you are in the console you can run/test below query against the neptune DB by opening local neptune repo.  
```
neptune> sparql PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX schema: <https://schema.org/> CONSTRUCT {<https://geoconnex.ca/id/catchment/02OJ*AB> ?p ?o. ?o ?p2 ?o2. <https://geoconnex.ca/id/catchment/02OJ*AB> ?p3 ?l} WHERE {<https://geoconnex.ca/id/catchment/02OJ*AB> ?p ?o. ?o ?p2 ?o2. <https://geoconnex.ca/id/catchment/02OJ*AB> ?p3 ?l. FILTER (isLiteral(?l))}
Evaluating SPARQL query...
```
## Commands to connect to Neptune:

To bulk upload data to the neptune database from S3 bucket, its hardcoded with lcnp-dev account variables, use the following commands:

```
curl -X POST \
    -H 'Content-Type: application/json' \
     https://geoconnex-dev-instance-1.cadlcqyheg76.ca-central-1.neptune.amazonaws.com:8182/loader -d '
    {
      "source" : "s3://geoconnex-data-dev/rdf/",
      "format" : "turtle",
      "iamRoleArn" : "arn:aws:iam::279053176446:role/neptune-load-data-role",
      "region" : "ca-central-1",
      "failOnError" : "FALSE",
      "parallelism" : "MEDIUM",
      "updateSingleCardinalityProperties" : "FALSE",
      "queueRequest" : "TRUE"
    }'
```
To check the status of the bulk upload, use the following command:
```
curl G 'https://geoconnex-dev-instance-1.cadlcqyheg76.ca-central-1.neptune.amazonaws.com:8182/loader/639a06d6-f68e-491d-b082-5635b949c00e'
```

### Sample Curl Query:
```
date;time curl -X POST "https://geoconnex-dev-instance-1.cadlcqyheg76.ca-central-1.neptune.amazonaws.com:8182/sparql" \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -H "Accept:application/sparql-results+json" \
   --data-urlencode 'format=json' \
   --data-urlencode 'default-graph-uri=http://www.example.com/ABC' \
   --data-urlencode 'query=PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX schema: <https://schema.org/> CONSTRUCT {<https://geoconnex.ca/id/catchment/02OJ*DC> ?p ?o. ?o ?p2 ?o2. <https://geoconnex.ca/id/catchment/02OJ*DC> ?p3 ?l} WHERE {<https://geoconnex.ca/id/catchment/02OJ*DC> ?p ?o. ?o ?p2 ?o2. <https://geoconnex.ca/id/catchment/02OJ*DC> ?p3 ?l. FILTER (isLiteral(?l))}' \
   --write-out '%{url_effective};%{http_code};%{time_total};%{time_namelookup};%{time_connect};%{size_download};%{speed_download}\n';date;
```
## Environemnt Variables
https://github.com/NRCan/gsip/blob/master/local.env
    
GSIP_APP=http://pub.gsip-dev.geo.ca/gsip

GSIP_BASEURI=http://localhost:8080

Incase of blazegraph:
GSIP_TRIPLESTORE=http://localhost:9999/bigdata/namespace/kb/sparql

Incase of Neptune: 
GSIP_TRIPLESTORE=https://geoconnex-dev-instance-1.cadlcqyheg76.ca-central-1.neptune.amazonaws.com:8182/sparql 