import logging
from datetime import datetime

from pythonjsonlogger import json

from app.config import settings
from app.utils.handlers import fileHandler, redis_handler


logger = logging.getLogger()


class CustomJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.now().isoformat()
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


json_formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

if not settings.MODE == "TEST":
    fileHandler.setFormatter(json_formatter)
    redis_handler.setFormatter(json_formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(redis_handler)

    logger.setLevel(settings.LOG_LVL)
