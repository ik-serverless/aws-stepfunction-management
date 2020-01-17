import boto3
import json


#set region
REGION = 'us-west-2'
#set the SNS topic ARN you want to alert on
SNS_TOPIC_ARN = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'

step = boto3.client('stepfunctions')

def get_state_machine(name=None):
    """
    Get a state machine given its name
    """
    response = step.list_state_machines()
    if not response.get('stateMachines'):
        return None
    for sm in response.get('stateMachines'):
        if sm['name'] == name:
            return sm['stateMachineArn']
        return response.get('stateMachines')

def get_executions(arn):
    """
    Get a state machine executions
    """
    response = step.list_executions(
        stateMachineArn=arn,
        statusFilter='RUNNING',
        maxResults=400
    )['executions']
    print(json.dumps(response, indent=2, sort_keys=True, default=j_serial))
    print(len(response))

def j_serial(o):     # self contained
    from datetime import datetime, date
    return str(o).split('.')[0] if isinstance(o, (datetime, date)) else None

def push_message(topic, message):
    sns_body = 'step functions running "{}", when suppose to be "{}", at "{}" UTC'.format(event['detail']['instance-id'], event['detail']['state'], event['time'])
    client = boto3.client('sns', region_name=REGION)
    response = client.publish(
        TopicArn=topic,
        Subject='Step Function State Change Notification',
        Message=message
    )

print(json.dumps(get_state_machine(), indent=2, sort_keys=True, default=j_serial))
for e in get_state_machine():
    get_executions(e['stateMachineArn'])

# write to logs as well how many step functions currently running