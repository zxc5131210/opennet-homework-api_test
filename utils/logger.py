import logging

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    :param name: logger name
    :param level: logging level
    :return: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        return logger
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
