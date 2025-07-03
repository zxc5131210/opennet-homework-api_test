import pytest
import logging
from api.cat_facts_client import CatFactsClient, CAT_FACTS_BASE_URL


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """
    Configures logging for the entire test session.
    'autouse=True' means this fixture is automatically used for all tests.
    """
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all messages

    # Create console handler and set level to info
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Only INFO and above to console
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Create file handler and set level to debug
    file_handler = logging.FileHandler('test_log.log', mode='w')  # 'w' for overwrite each run
    file_handler.setLevel(logging.DEBUG)  # All DEBUG messages to file
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Add handlers to the logger
    # Ensure no duplicate handlers if pytest re-runs parts of setup
    if not logger.handlers:  # Only add handlers if they don't already exist
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    # Optional: Prevent requests library from cluttering logs if too verbose
    # logging.getLogger("requests").setLevel(logging.WARNING)
    # logging.getLogger("urllib3").setLevel(logging.WARNING)

    logger.info("Logging configured for test session.")

    # Yield control to tests, then clean up handlers after tests are done
    yield

    logger.info("Test session finished. Logging handlers removed.")
    # Clean up handlers to prevent issues with multiple test runs in the same process
    for handler in logger.handlers[:]:  # Iterate over a slice to avoid modification issues
        handler.close()
        logger.removeHandler(handler)


@pytest.fixture(scope="session")
def cat_facts_client() -> CatFactsClient:
    """
    Provides a CatFactsClient instance for tests.
    """
    return CatFactsClient(base_url=CAT_FACTS_BASE_URL)