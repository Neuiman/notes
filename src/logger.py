import logging


file_handler = logging.FileHandler("/notes/logs/app.log")
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    "- %(pathname)s:%(lineno)d"
))
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

logger.addHandler(file_handler)

