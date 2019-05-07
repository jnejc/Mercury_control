'''Test using of logger from different module'''

#from logger import my_logger
import logger    # Done once in main?

import logging
my_logger = logging.getLogger('log')     # Works in any module
# Alternatively:
#from logger import my_logger    # Path is module dependent...

my_logger.debug('I am debugging')
my_logger.info('I am informing')
my_logger.warning('I am warning you!')
my_logger.error('This is an error!')
my_logger.critical('Holy shit things are going critical!!!!')

# This configuration seems to work.
