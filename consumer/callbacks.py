from log import logger


def user_info_callback(ch, method, properties, body):
    del ch, method, properties
    logger.info(f"user_info: {body.decode('UTF-8')}")

def user_error_callback(ch, method, properties, body):
    del ch, method, properties
    logger.error(f"user_error: {body.decode('UTF-8')}")

def oder_info_callback(ch, method, properties, body):
    del ch, method, properties
    logger.info(f"oder_info: {body.decode('UTF-8')}")

def oder_error_callback(ch, method, properties, body):
    del ch, method, properties
    logger.error(f"oder_error: {body.decode('UTF-8')}")
