from __future__ import absolute_import, unicode_literals
from boto3.dynamodb.conditions import Key
import boto3
from celery import shared_task
from celery.utils.log import get_task_logger
import datetime
import uuid


logger = get_task_logger(__name__)

# Tasks


@shared_task
def build_reports_last_minutes(minutes):
    """
    Task to create reports based on last minutes
    :param minutes: The time will be between now and now - minutes
    :return:
    """
    table = _get_table('chatbook-events')
    d_end = datetime.datetime.now()
    d_start = d_end - datetime.timedelta(minutes=minutes)

    start = d_start.strftime("%Y-%m-%dT%H:%M:%S%z.%f") + "+09:00"  # TODO: For the test
    end = d_end.strftime("%Y-%m-%dT%H:%M:%S%z.%f") + "+09:00"  # TODO: For the test

    entries = _query_between_dates(table, start, end)
    logger.info("####### Start date {} => End date {} #######".format(start, end))
    logger.info("####### {} Entries found #######".format(len(entries['Items'])))

    d_now = datetime.datetime.now()
    now = d_now.strftime("%Y-%m-%dT%H:%M:%S%z.%f") + "+09:00"

    build_visitor_reports(entries['Items'], now)
    build_individual_visitor_reports(entries['Items'], now)
    logger.info("REPORTS CREATED")


@shared_task
def build_reports_from_22_to_25():
    """
    Dummy Task to get reports from events.json
    :return:
    """
    table = _get_table('chatbook-events')
    start = "2019-06-22T00:00:00.000000+09:00"
    end = "2019-06-25T00:00:00.000000+09:00"

    entries = _query_between_dates(table, start, end)
    logger.info("####### Start date {} => End date {} #######".format(start, end))
    logger.info("####### {} Entries found #######".format(len(entries['Items'])))

    d_now = datetime.datetime.now()
    now = d_now.strftime("%Y-%m-%dT%H:%M:%S%z.%f") + "+09:00"

    build_visitor_reports(entries['Items'], now)
    build_individual_visitor_reports(entries['Items'], now)
    logger.info("REPORTS CREATED")


# Build Reports


def build_visitor_reports(entries, now):
    """
    From events found in the DB, create and store Visitor reports
    :param entries: Items from dynamoDB (list)
    :param now: Date now (string, ISO)
    :return:
    """
    if not entries:
        return

    d_visitors = {}
    for entry in entries:
        if entry['visitor'] not in d_visitors:
            d_visitors[entry['visitor']] = [entry]
        else:
            d_visitors[entry['visitor']].append(entry)

    l_reports = []
    for visitor, l_entries in d_visitors.items():
        report = {}
        report["n_interactions"] = len(l_entries)
        first_entry = l_entries[0]
        report['uuid'] = str(uuid.uuid1())
        report['visitor'] = visitor
        report['adblock'] = first_entry['adblock']
        report['ip_address'] = first_entry['ip_address']
        report['user_agent'] = first_entry['user_agent']
        report['language'] = first_entry['language']
        report['timestamp'] = now
        l_reports.append(report)

    table = _get_table('chatbook-visitor-reports')
    for report in l_reports:
        table.put_item(
            Item=report
        )


def build_individual_visitor_reports(entries, now):
    """
    From events, create and store individual visitor events reports
    :param entries: Items from dynamoDB (list)
    :param now: Date now (string, ISO)
    :return:
    """
    if not entries:
        return
    l_reports = []

    for entry in entries:
        report = {
            "page": entry['pathname'],
            "action": "action",
            "request_id": entry['request_id'],
            "timestamp": now
        }
        l_reports.append(report)

    table = _get_table('chatbook-events-reports')
    for report in l_reports:
        table.put_item(
            Item=report
        )
    return

# TOOLS


def _get_table(table_name):
    """
    From a given name, get a dynamoDB table
    :param table_name: table name in AWS (string)
    :return: DynameDB table (Table)
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table


def _query_between_dates(table, start, end):
    """
    Get the entries from a DynamoDB table which where created between two dates
    :param table: DynameDB table (Table)
    :param start: starting date (string)
    :param end: ending date (string)
    :return:
    """
    fe = Key('created').between(start, end)
    entries = table.scan(
        FilterExpression=fe
    )
    return entries
