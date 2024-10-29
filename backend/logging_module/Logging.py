# Copyright 2024. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from logging import handlers

from backend.constants.constants import CONTAINER_MOUNT_POINT, LOG_FORMATTER


class Logging:
    threadPoolSize = 5
    executor = ThreadPoolExecutor(max_workers=threadPoolSize)

    log_location = CONTAINER_MOUNT_POINT
    try:
        os.makedirs(log_location)
    except FileExistsError:
        print(f"File already created, skipping creation of {log_location}")

    log_file_max_size = 52428800  # bytes = 50 MiB
    max_log_file_count = 10
    log_formatter = LOG_FORMATTER

    def __init__(self, service_name):
        """
        Constructor to initialize the logger if the logger is not already available. Logger will only be created once
        and reused by all subsequent calls
        :param service_name: Name of the microservice creating this logger.
        """
        self.service_name = service_name
        if not logging.getLogger(service_name).hasHandlers():
            self.logger = logging.getLogger(service_name)
            self.level = logging.INFO

            self.logger.setLevel(self.level)

            formatter = logging.Formatter(self.log_formatter)

            # filename set to service name passed by the user
            log_file_name = f"{self.log_location}{service_name}.log"

            # this handler will write to console
            console_handler = logging.StreamHandler()
            # this handler will create at max 10 files and rotate the logs in those files
            file_handler = handlers.RotatingFileHandler(
                log_file_name,
                maxBytes=self.log_file_max_size,
                backupCount=self.max_log_file_count,
            )
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message):
        # add the trace message to file
        self.logger.info(message)

    def debug(self, message):
        # add the trace message to file
        self.logger.debug(message)

    def error(self, message, exp: BaseException):
        # add the trace message to file
        self.logger.error(message, exc_info=exp)

    def warning(self, message, exp: BaseException):
        # add the trace message to file
        self.logger.warning(message, exc_info=exp)
