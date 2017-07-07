import daiquiri
import daiquiri.formatter
import logging
import sys
import test_print_log_sub_module

log_file = sys.path[0] + "/test.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.Stream(formatter=daiquiri.formatter.ColorFormatter(
            fmt="%(asctime)s [PID %(process)d] [%(levelname)s] "
                "%(name)s:%(lineno)d %(message)s")),
        daiquiri.output.File(log_file,
                             formatter=daiquiri.formatter.ColorFormatter(
                                 fmt="%(asctime)s [PID %(process)d] "
                                     "[%(levelname)s] %(name)s:%(lineno)d "
                                     "%(message)s")),
    )
)

logger = daiquiri.getLogger(__name__)

if __name__ == "__main__":
    logger.info("log some info")
    logger.warning("log some warning")
    logger.error("log some error")
    logger.debug("log some debug")
    logger.info("some data is:%s" % ("testdata"))
    test_print_log_sub_module.print_log()
