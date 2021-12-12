"""
Function for creating or deleting S3 buckets. AWS S3 doesn't allow deleting buckets that 
are not empty. If you create a S3 resource as part of Cloudformation, deleting it will fail
when you delete the stack. This function can be used as a custom resource in Cloudformation
for creating/deleting s3 buckets. 

--- Cloudformation resource parameters ---

BucketName: required - Name of the S3 bucket to create/delete

"""
import boto3
import logging
import os
from functions.cfn_resource import Resource

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = Resource()


@handler.delete
def lambda_handler_delete(event, context):
    properties = event['ResourceProperties']
    s3_bucket_name = properties['BucketName'].lower()

    try:
        s3 = boto3.resource('s3')
        try:
            s3_bucket = s3.Bucket(s3_bucket_name)
            s3_bucket.objects.delete()
            s3_bucket.delete()
            logger.info("S3 bucket {} deleted.".format(s3_bucket_name))
        except Exception as e:
            logger.info('Failed to delete S3 bucket {}. {}'.format(
                s3_bucket_name, e))

        return {
            'Status': 'SUCCESS',
            'Reason': 'Bucket deleted',
            'PhysicalResourceId': context.log_stream_name,
            'StackId': event['StackId'],
            'RequestId': event['RequestId'],
            'LogicalResourceId': event['LogicalResourceId'],
            'Data': {}
        }
    except Exception as e:
        error_msg = 'Error: {}'.format(e)
        logger.error(error_msg)

        return {
            'Status': 'FAILED',
            'Reason': error_msg,
            'PhysicalResourceId': context.log_stream_name,
            'StackId': event['StackId'],
            'RequestId': event['RequestId'],
            'LogicalResourceId': event['LogicalResourceId']
        }


@handler.update
@handler.create
def lambda_handler(event, context):
    properties = event['ResourceProperties']
    s3_bucket_name = properties['BucketName'].lower()

    try:
        s3 = boto3.client('s3')
        region = os.environ["AWS_DEFAULT_REGION"]

        s3.create_bucket(
            ACL='private',
            Bucket=s3_bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
        s3.put_public_access_block(
            Bucket=s3_bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        return {
            'Status': 'SUCCESS',
            'Reason': 'Bucket created',
            'PhysicalResourceId': context.log_stream_name,
            'StackId': event['StackId'],
            'RequestId': event['RequestId'],
            'LogicalResourceId': event['LogicalResourceId'],
            'Data': {
                'Value': s3_bucket_name
            }
        }
    except Exception as e:
        error_msg = 'Error: {}'.format(e)
        logger.error(error_msg)

        return {
            'Status': 'FAILED',
            'Reason': error_msg,
            'PhysicalResourceId': context.log_stream_name,
            'StackId': event['StackId'],
            'RequestId': event['RequestId'],
            'LogicalResourceId': event['LogicalResourceId']
        }
