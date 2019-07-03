import logging
import logging.config
import yaml

with open('../log_config.yml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def getLogger(name: str):
    return logging.getLogger(name)


def test_logger():
    log = getLogger("TestClass")
    log.debug("1- This is a debug")
    log.info("2- This is a info")
    log.warning("3- This is a warn")
    log.error("4- This is an error")
    log.critical("5- this is critical")


if __name__ == '__main__':
    test_logger()
