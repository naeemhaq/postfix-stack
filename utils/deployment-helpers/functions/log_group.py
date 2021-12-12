"""
Function that creates a CloudWatch LogGroup with a given name. If the LogGroup already
exists, it will not do anything and will not raise any error.

--- Cloudformation resource parameters ---

LogGroupName: required - Name of the Cloudwatch log group to create.

RetentionInDays: required - Log group retention in days.

SubscriptionDestinationArn: ARN of the subscription destination.

SubscriptionFilterName: conditional - Subscription filter name. This parameter is only required if SubscriptionDestinationArn is set.

SubscriptionFilterPattern: Subscription filter pattern.

--- Lambda permissions required ---
- logs:CreateLogGroup
- logs:PutRetentionPolicy
- logs:DescribeSubscriptionFilters
- logs:DescribeLogGroups
- logs:DeleteSubscriptionFilter
- logs:PutSubscriptionFilter
"""
import boto3
import logging
from functions.cfn_resource import Resource

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = Resource()


@handler.update
@handler.create
def lambda_handler(event, context):
    properties = event['ResourceProperties']
    log_group_name = properties['LogGroupName']
    retention_in_days = int(properties['RetentionInDays'])
    subscription_destination_arn = properties.get('SubscriptionDestinationArn')
    subscription_filter_pattern = properties.get(
        'SubscriptionFilterPattern', '')
    subscription_filter_name = properties.get('SubscriptionFilterName')
    add_filter = True

    try:
        client = boto3.client('logs')
        try:
            client.create_log_group(
                logGroupName=log_group_name
            )
        except client.exceptions.ResourceAlreadyExistsException as e:
            logger.info('Log group {} already exists.'
                        .format(log_group_name))
        client.put_retention_policy(
            logGroupName=log_group_name,
            retentionInDays=retention_in_days
        )
        # Clear all existing subscription filters
        next_token = ''
        filters = []
        while True:
            if next_token:
                result = client.describe_subscription_filters(
                    logGroupName=log_group_name,
                    nextToken=next_token
                )
            else:
                result = client.describe_subscription_filters(
                    logGroupName=log_group_name
                )

            filters.extend(result['subscriptionFilters'])
            if 'nextToken' in result:
                next_token = result['nextToken']
            else:
                break
        for item in filters:
            if item['filterName'] == subscription_filter_name:
                add_filter = False

        # Add new subscription filter if the parameter is set
        if subscription_destination_arn and add_filter:
            try:
                client.put_subscription_filter(
                    logGroupName=log_group_name,
                    filterName=subscription_filter_name,
                    filterPattern=subscription_filter_pattern,
                    destinationArn=subscription_destination_arn
                )
            except Exception as e:
                error_msg = 'Error: {}'.format(e)
                logger.error(error_msg)
        log_groups_result = client.describe_log_groups(
            logGroupNamePrefix=log_group_name,
            limit=1
        )

        return {
            'Status': 'SUCCESS',
            'Reason': 'Log group created',
            'PhysicalResourceId': context.log_stream_name,
            'StackId': event['StackId'],
            'RequestId': event['RequestId'],
            'LogicalResourceId': event['LogicalResourceId'],
            'Data': {
                'Value': log_group_name,
                'Arn': log_groups_result.get('logGroups')[0].get('arn')
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


@handler.delete
def lambda_handler(event, context):
    properties = event['ResourceProperties']
    log_group_name = properties['LogGroupName']
    subscription_filter_name = properties.get('SubscriptionFilterName')

    return {
        'Status': 'SUCCESS',
        'Reason': 'Log subscription deleted',
        'PhysicalResourceId': context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': {
            'Value': log_group_name
        }
    }
    # try:
    #     client = boto3.client('logs')

    #     # Clear all existing subscription filters
    #     next_token = ''
    #     filters = []
    #     while True:
    #         if next_token:
    #             result = client.describe_subscription_filters(
    #                 logGroupName=log_group_name,
    #                 nextToken=next_token
    #             )
    #         else:
    #             result = client.describe_subscription_filters(
    #                 logGroupName=log_group_name
    #             )

    #         filters.extend(result['subscriptionFilters'])
    #         if 'nextToken' in result:
    #             next_token = result['nextToken']
    #         else:
    #             break
    #     for item in filters:
    #         if item['filterName'] == subscription_filter_name:
    #             client.delete_subscription_filter(
    #                 logGroupName=log_group_name,
    #                 filterName=item['filterName']
    #             )

    #     return {
    #         'Status': 'SUCCESS',
    #         'Reason': 'Log subscription deleted',
    #         'PhysicalResourceId': context.log_stream_name,
    #         'StackId': event['StackId'],
    #         'RequestId': event['RequestId'],
    #         'LogicalResourceId': event['LogicalResourceId'],
    #         'Data': {
    #             'Value': log_group_name
    #         }
    #     }
    # except Exception as e:
    #     error_msg = 'Error: {}'.format(e)
    #     logger.error(error_msg)

    #     return {
    #         'Status': 'FAILED',
    #         'Reason': error_msg,
    #         'PhysicalResourceId': context.log_stream_name,
    #         'StackId': event['StackId'],
    #         'RequestId': event['RequestId'],
    #         'LogicalResourceId': event['LogicalResourceId']
    #     }
