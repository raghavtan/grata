import os
import re
import sys
import time

import boto3

from src.resources.rds.mysql_parser import SlowQueryLog
from numba import jit

client = boto3.client('rds')


def fetch_all_rds():
    """

    :return:
    """
    identifiers_list = []
    response = client.describe_db_instances()
    for instance in response["DBInstances"]:
        if "limetraycms" in instance["DBInstanceIdentifier"]:
            identifiers_list.append(instance["DBInstanceIdentifier"])
    return identifiers_list


# Iterate through list of log files and print out the entries
@jit(nopython=True)
def getlogs(instance_identifier, days_to_ingest):
    """

    :param instance_identifier:
    :param days_to_ingest:
    :return:
    """
    if len(sys.argv) > 1:
        instance_identifier = sys.argv[1]

    lastReadDate = int(round(time.time() * 1000)) - ((1000 * 60 * 60 * 24) * days_to_ingest)
    readState = {}

    # Wait for the instance to be available -- need to possibly fix this or replace it with a custom waiter
    # client.get_waiter('db_instance_available').wait(DBInstanceIdentifier=dBInstanceIdentifier)
    # Get a list of the logs that have been modified since last run
    dbLogs = client.describe_db_log_files(
        DBInstanceIdentifier=instance_identifier,
        FileLastWritten=lastReadDate,  # Base this off of last query
    )
    combined_log = ""
    for logFile in dbLogs['DescribeDBLogFiles']:
        if logFile['LogFileName'] in readState:
            readMarker = readState[logFile['LogFileName']]
        else:
            readMarker = '0'
        ext = ['xel', 'trc']  # Ignore binary data log files for MSSQL
        if not logFile['LogFileName'].endswith(tuple(ext)):
            # Also may need to fix this waiter
            # client.get_waiter('db_instance_available').wait(
            #    DBInstanceIdentifier=dBInstanceIdentifier,
            # )
            response = client.download_db_log_file_portion(
                DBInstanceIdentifier=instance_identifier,
                LogFileName=logFile['LogFileName'],
                Marker=readMarker,
            )
            if len(response['LogFileData']) > 0:
                if "slowquery" in logFile['LogFileName']:
                    combined_log += response['LogFileData']
    return combined_log


@jit(nopython=True)
def sanitize(log_str):
    """

    :param log_str:
    :return:
    """
    removal_lines = ["^/rdsdbbin/mysql/bin/mysqld.*",
                     "^Tcp port: 3306.*",
                     r"Time.+Argument",
                     "^#\s+Time:\s+\d+\s+\d+:\d+:\d+"]
    for removal in removal_lines:
        log_str = re.sub(removal, '', log_str, flags=re.MULTILINE)
    return "".join([s for s in log_str.strip().splitlines(True) if s.strip("\r\n").strip()])


@jit(nopython=True)
def split(log_file, splitter):
    """

    :param log_file:
    :param splitter:
    :return:
    """
    log_file = log_file.replace(splitter, "__SPLIT__%s" % splitter)
    events = log_file.split("__SPLIT__")
    return events


@jit(nopython=True)
def parse_log(event):
    """

    :param event:
    :return:
    """
    event_list = {}
    f = open('_tmp_event', 'w')
    f.write(event)
    f.close()
    f_new = open('_tmp_event', 'r')
    loggy = SlowQueryLog(f_new)
    for k, v in loggy.next().items():
        event_list[k] = v
    f_new.close()
    os.remove("_tmp_event")
    return event_list


@jit(nopython=True)
def parsed_events(dBInstanceIdentifier, days_to_ingest):
    queries_parsed = []
    previous_database = None
    slow_logs = sanitize(getlogs(dBInstanceIdentifier, days_to_ingest))
    events = split(slow_logs, "# User@Host:")
    for event in events:
        if len(event) > 1:
            EVENT = {"query_time": None,
                     "rows_examined": None,
                     "rows_sent": None,
                     "database": None,
                     "rows_read": None,
                     "lock_time": None,
                     "session_id": None,
                     "datetime": None,
                     "host": None,
                     "user": None,
                     "query": None,
                     "rows_affected": None}
            temp = parse_log(event)
            for element in EVENT.keys():
                if element in temp.keys():
                    EVENT[element] = temp[element]
                    if element == "database" and temp[element]:
                        previous_database = temp[element]

                    elif element == "database" and not temp[element]:
                        EVENT[element] = previous_database

            queries_parsed.append(EVENT)
    return queries_parsed