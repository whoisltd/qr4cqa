import datetime
import json
import logging
import os
from logging.config import dictConfig

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


def setup_logging_json(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    :param default_path:
    :param default_level:
    :param env_key:
    :return:
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
            dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def format_date_time(date):
    if isinstance(date, datetime.datetime):
        return date.strftime(DATE_TIME_FORMAT)
    else:
        return date


def format_date(date):
    if isinstance(date, datetime.datetime) or isinstance(date, datetime.date):
        return date.strftime(DATE_FORMAT)
    else:
        return date


def parse_date_time(string):
    if isinstance(string, datetime.datetime) or isinstance(string, datetime.date):
        return string
    try:
        return datetime.datetime.strptime(string, DATE_TIME_FORMAT)
    except:
        return None


def parse_date(string):
    try:
        return datetime.datetime.strptime(string, DATE_FORMAT)
    except:
        return None


def iter_sub_list(input_list, batch_size=10):
    num_batch = int((len(input_list) - 1) / batch_size + 1)
    for i in range(num_batch):
        yield input_list[i * batch_size: (i + 1) * batch_size]
