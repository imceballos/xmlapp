from logger import Logger

logger = Logger(__name__)

data = (logger.logging_date_range("app.log", '2023-04-29 03:30:00,000', '2023-04-29 04:00:03,162'))
data2 = logger.logging_type(data, 'INFO')
data3 = logger.logging_description(data2, 'out')
