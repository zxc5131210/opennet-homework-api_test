import requests
import logging


CAT_FACTS_BASE_URL = "https://catfact.ninja"


class CatFactsClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        logging.info(f"CatFactsClient initialized with base URL: {self.base_url}")

    def _make_get_request(self, endpoint: str, params: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"

        logging.debug(f"Sending GET request to: {url}")
        if params:
            logging.debug(f"Request parameters: {params}")

        response = requests.get(url, params=params)

        logging.info(
            f"Received response from {url} with status code: {response.status_code}"
        )
        logging.debug(f"Response headers: {response.headers}")
        logging.debug(f"Response body: {response.text}")

        response.raise_for_status()

        return response.json()

    def get_single_fact(self) -> dict:
        logging.info("Fetching single cat fact.")
        return self._make_get_request(endpoint="/fact")

    def get_multiple_facts(self, limit: int = None, max_length: int = None) -> dict:
        log_msg = "Fetching multiple cat facts"
        if limit:
            log_msg += f" with limit={limit}"
        if max_length:
            log_msg += f" with max_length={max_length}"
        logging.info(log_msg)
        return self._make_get_request(
            endpoint="/facts", params={"limit": limit, "max_length": max_length}
        )
