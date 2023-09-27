import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create file handler on Container or Local structure
try:
    log_handler = logging.FileHandler('./logs/consumer.log')
except FileNotFoundError:
    log_handler = logging.FileHandler('./consumer.log')

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
