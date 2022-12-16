import functools
import sys
import traceback

from loguru import logger

from src.services.logging.config import ROTATION_CONDITITON

logger.remove(0)


def add_to_file_logs():
    logger.add('logs.txt',
               compression='zip',
               rotation=ROTATION_CONDITITON)


def add_usually_logs():

    def my_filter(message):
        return (message['level'].name in ('INFO', 'DEBUG', 'WARNING', 'ERROR', 'SUCCESS', 'CRITICAL')
                and ('task' not in message['extra'] or message['extra']['task'] != 'middleware'))

    logger.add(sys.stdout,
               filter=my_filter,
               colorize=True)


def add_middleware_level():
    logger.add(sys.stdout,
               format='<green>[{time:DD-MM-YYYY HH:mm:ss.SSS]}</> <red>| Middleware |</> <b>{message}</>',
               filter=lambda record: 'task' in record['extra'] and record["extra"]["task"] == 'middleware',
               # filter=lambda message: print(message['extra']),
               colorize=True)


add_usually_logs()
add_middleware_level()
add_to_file_logs()


def logging(function=None,
            entry: bool = True,
            exit: bool = False,
            level: str = "DEBUG",
            error: bool = False):
    """
        My decorator for logging
    :param function: function which need to decor
    :param entry: output entry data yes or not
    :param exit: output return data yes or not
    :param level: level of logging
    :return:
    """
    if function is None:
        return functools.partial(logging,
                                 entry=entry,
                                 exit=exit,
                                 level=level,
                                 error=error)

    @functools.wraps(function)
    def wrapper(*args, **kwargs):

        function_name = function.__name__
        logger_ = logger.opt(depth=1)

        if entry:
            logger_.log(level, "Entering '{}' (args={}, kwargs={})", function_name, args, kwargs)

        try:
            result = function(*args, **kwargs)

        except Exception as e:
            if error:
                logger.exception(e)
            return

        if exit:
            logger_.log(level, "Exiting '{}' (result={})", function_name, result)

        return result

    return wrapper


def create_exception_log() -> str:
    """
        Error output
    :return: error in str format
    """
    error = traceback.format_exc(limit=1)
    logger.error(error)
    return error

