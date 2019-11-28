import logging
import os

log = logging.getLogger(__file__)


class FileLogger:

    def __init__(self):
        self.directory = os.path.join(os.getcwd(), "out", "certif")
        if os.path.exists(self.directory) is False:
            os.mkdir(self.directory)
        self.counter = 0

    def log_data(self, data, name, binary: bool = False, increment: bool = False):
        if increment is True:
            self.counter += 1
        file_path = os.path.join(self.directory, f"{self.counter}-{name}")
        print(f"type of data: {type(data)}")
        with open(file_path, f"w{'b' if binary else 't'}") as file:
            file.write(data)
            file.close()
        log.info(f"data succesfully logged to {file_path}")
