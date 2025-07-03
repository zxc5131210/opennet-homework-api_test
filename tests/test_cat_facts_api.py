import pytest
import logging

# Get logger for this test file
logger = logging.getLogger(__name__)


def test_get_single_cat_fact(cat_facts_client):
    logger.info("Starting test: TC_CF_001 - Get a single random cat fact.")

    data = cat_facts_client.get_single_fact()

    assert "fact" in data
    assert "length" in data
    assert isinstance(data["fact"], str)
    assert isinstance(data["length"], int)

    assert len(data["fact"].strip()) == data["length"], \
        f"Fact length mismatch (after stripping whitespace): Expected {data['length']}, got {len(data['fact'].strip())}. Original fact: '{data['fact']}'"

    logger.info("Test TC_CF_001 completed successfully.")


@pytest.mark.parametrize("limit, max_length, expected_data_count_min", [
    (None, None, 1),
    (3, None, 3),
    (None, 50, 1),
    (2, 30, 2),
])
def test_get_multiple_cat_facts(cat_facts_client, limit, max_length, expected_data_count_min):
    test_id = f"TC_CF_{3 if limit is not None else (4 if max_length is not None else 2)}"  # Simple logic for test ID approximation
    if limit is not None and max_length is not None:
        test_id = "TC_CF_005"

    params_str = f"limit={limit}, max_length={max_length}" if limit is not None or max_length is not None else "default"
    logger.info(f"Starting test: {test_id} - Get multiple cat facts with parameters: {params_str}")

    data = cat_facts_client.get_multiple_facts(limit=limit, max_length=max_length)

    assert "data" in data
    assert isinstance(data["data"], list)

    if limit is not None:
        assert len(data["data"]) == limit, \
            f"Expected fact count to be {limit}, but got {len(data['data'])}. Parameters: {params_str}"
    else:
        assert len(data["data"]) >= expected_data_count_min, \
            f"Expected at least {expected_data_count_min} fact(s), but got {len(data['data'])}. Parameters: {params_str}"

    if len(data["data"]) == 0 and expected_data_count_min > 0:
        pytest.fail(
            f"Fact list is empty, but expected at least {expected_data_count_min} fact(s). Parameters: {params_str}")

    for fact_item in data["data"]:
        assert "fact" in fact_item
        assert "length" in fact_item
        assert isinstance(fact_item["fact"], str)
        assert isinstance(fact_item["length"], int)

        assert len(fact_item["fact"].strip()) == fact_item["length"], \
            f"Fact length mismatch (after stripping whitespace): Expected {fact_item['length']}, got {len(fact_item['fact'].strip())}. Original fact: '{fact_item['fact']}'"

        if max_length is not None:
            assert fact_item["length"] <= max_length, \
                f"Fact length {fact_item['length']} exceeds max_length {max_length}. Fact: '{fact_item['fact']}'"

    logger.info(f"Test {test_id} completed successfully.")