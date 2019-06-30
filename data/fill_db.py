import boto3
import json


def create_table_events_reports_table(table_name="chatbook-events-reports"):
    dynamodb_client = boto3.client('dynamodb')
    try:
        table = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'request_id',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'request_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("START CREATION")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    except:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        print("INFO: {} already exists".format(table_name))
    return table


def create_table_reports_table(table_name="chatbook-visitor-reports"):
    dynamodb_client = boto3.client('dynamodb')
    try:
        table = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("START CREATION")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    except:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        print("INFO: {} already exists".format(table_name))
    return table


def create_table_events(table_name="chatbook-events"):
    dynamodb_client = boto3.client('dynamodb')
    try:
        table = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'request_id',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'request_id',
                    'AttributeType' : 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("START CREATION")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    except:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        print("INFO: {} already exists".format(table_name))
    return table


def get_events_from_json(filename="events.json"):
    l_events = []
    with open(filename, 'r') as f:
        d_events = json.load(f)

    id = d_events['id']
    name = d_events['name']

    properties = d_events['properties']
    for prop in properties:
        property = prop

        info = properties[prop]
        domain = info['domain']
        provider = info['provider']
        type = info['type']

        for vis in info['visitors']:
            visitor = vis

            visitor_info = info['visitors'][vis]

            for event in visitor_info['events']:
                new_event = {}
                new_event.update(event)
                new_event['id'] = id
                new_event['name'] = name
                new_event['property'] = property
                new_event['domain'] = domain
                new_event['type'] = type
                new_event['visitor'] = visitor
                new_event['provider'] = provider
                l_events.append(new_event)
    return l_events


def fill_table(table, l_events):
    for event in l_events:
        table.put_item(
            Item=event
        )


def main():
    _ = create_table_events_reports_table()
    _ = create_table_reports_table()
    table_events = create_table_events()
    l_events = get_events_from_json()
    fill_table(table_events, l_events)


main()
