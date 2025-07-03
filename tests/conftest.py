import pytest
from api.cat_facts_client import CatFactsClient, CAT_FACTS_BASE_URL


@pytest.fixture(scope="session")
def cat_facts_client() -> CatFactsClient:
    """
    Provides a CatFactsClient instance for tests.
    """
    return CatFactsClient(base_url=CAT_FACTS_BASE_URL)