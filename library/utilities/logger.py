import logging


# Implemented very basic logging for now so that modules can use it.
# TODO: Modify this to use a proper logging module
def get_logger(logger_name):
    logging.basicConfig(level=logging.DEBUG)
    return logging


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Hello Information")
    logger.debug("Hello debug")
    logger.warning("Hello warning")
