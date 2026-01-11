import logging
import sys

from books_api.utils import setup_logging


class TestSetupLogging:
    def test_returns_logger(self):
        logger = setup_logging()
        assert isinstance(logger, logging.Logger)

    def test_logger_name(self):
        logger = setup_logging()
        assert logger.name == "books_api"

    def test_default_level(self):
        logger = setup_logging()
        assert logger.level == logging.INFO

    def test_custom_level(self):
        logger = setup_logging(level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_has_handler(self):
        logger = setup_logging()
        assert len(logger.handlers) > 0

    def test_handler_is_stream_handler(self):
        logger = setup_logging()
        handler = logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

    def test_handler_outputs_to_stdout(self):
        logger = setup_logging()
        handler = logger.handlers[0]
        assert handler.stream == sys.stdout

    def test_no_duplicate_handlers(self):
        logger = setup_logging()
        initial_count = len(logger.handlers)
        setup_logging()
        assert len(logger.handlers) == initial_count
