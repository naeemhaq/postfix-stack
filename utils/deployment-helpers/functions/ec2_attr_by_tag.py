"""
Function that searches EC2 instances to find one with the specified Filter. 
If AttrName is set, it'll return the value for EC2 instance attribute.
If TagName is set, it'll return the value for the specified Tag name. 
"""
import boto3
import logging
import json
from functions.cfn_resource import Resource

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = Resource()


@handler.update
@handler.create
def lambda_handler(event, context):
    properties = event['ResourceProperties']
    search = json.loads(properties['Filter'])
    attr_name = properties['AttrName'] if 'AttrName' in properties.keys(
    ) else None
    tag_name = properties['TagName'] if 'TagName' in properties.keys(
    ) else None
    value = None

    try:
        if(attr_name is None and tag_name is None):
            raise Exception('Either AttrName or TagName must be given.')
        if(attr_name is not None and tag_name is not None):
            raise Exception('Only one of AttrName or TagName must be given.')

        client = boto3.client('ec2')
        response = client.describe_instances(Filters=[
            {'Name': 'tag:{}'.format(search['Tag']['Name']), 'Values': [
                search['Tag']['Value']]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ])
        for r in response['Reservations']:
            for i in r['Instances']:
                if tag_name is not None:
                    for t in i['Tags']:
                        if t['Key'] == tag_name:
                            value = t['Value']
                else:
                    value = i[attr_name]

        if value is None:
            raise Exception('Unable to get EC2 attribute: {}'.format(
                tag_name if tag_name is not None else attr_name)
            )

        logger.info('Filter-> {}, AttrName-> {}, TagName-> {}'
                    .format(search, attr_name, tag_name))
        return {
            'Status': 'SUCCESS',
            'Reason': 'Parameter found',
            'PhysicalResourceId': context.log_stream_name,
            'StackId': event['StackId'],
            'RequestId': event['RequestId'],
            'LogicalResourceId': event['LogicalResourceId'],
            'Data': {
                'Value': value
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
