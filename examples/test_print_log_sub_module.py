import daiquiri


logger = daiquiri.getLogger(__name__)


def print_log():
    logger.info("log in sub-module")
