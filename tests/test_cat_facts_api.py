from typing import Optional

import allure
import pytest
import logging


@allure.description(
    """
    1. Check status code
    2. Check response JSON structure and data types
    3. Validate fact length matches length value (after stripping whitespace)
    """
)
@allure.feature("Cat Facts API")
@allure.story("Get single facts with parameters")
@pytest.mark.case1
def test_get_single_cat_fact(cat_facts_client):

    data = cat_facts_client.get_single_fact()

    assert "fact" in data
    assert "length" in data
    assert isinstance(data["fact"], str)
    assert isinstance(data["length"], int)

    assert len(data["fact"]) == data["length"], (
        f"Fact length mismatch (after stripping whitespace): Expected {data['length']}, got {len(data['fact'].strip())}."
        f" Original fact: '{data['fact']}'"
    )

    logging.info("Test TC_CF_001 completed successfully.")


@allure.title("Test Get Multiple Cat Facts with Various Parameters")
@pytest.mark.parametrize(
    "limit, max_length, expected_data_count_min",
    [
        pytest.param(None, None, 1, marks=pytest.mark.case2),  # type: ignore
        pytest.param(3, None, 3, marks=pytest.mark.case3),  # type: ignore
        pytest.param(None, 50, 1, marks=pytest.mark.case4),  # type: ignore
        pytest.param(2, 30, 2, marks=pytest.mark.case5),  # type: ignore
        pytest.param(-1, None, 0, marks=pytest.mark.case6),  # negative
    ],
    ids=["default", "limit_3", "maxlen_50", "limit_2_maxlen_30", "invalid_params"],
)
def test_get_multiple_cat_facts(
    cat_facts_client,
    limit: Optional[int],
    max_length: Optional[int],
    expected_data_count_min: int,
):
    params_str = (
        f"limit={limit}, max_length={max_length}" if limit or max_length else "default"
    )
    allure.dynamic.description(
        f"Validate the /facts endpoint with parameters: {params_str}"
    )

    test_id = (
        "TC_CF_006"
        if limit == -1
        else (
            f"TC_CF_{3 if limit is not None else (4 if max_length is not None else 2)}"
        )
    )
    if limit is not None and max_length is not None and limit != -1:
        test_id = "TC_CF_005"

    logging.info(
        f"Starting test: {test_id} - Get multiple cat facts with parameters: {params_str}"
    )

    data = cat_facts_client.get_multiple_facts(limit=limit, max_length=max_length)

    if limit == -1:
        with allure.step("Verify API returns error for invalid parameters"):
            assert (
                "data" not in data or not data["data"]
            ), f"Expected error or empty data for invalid parameters, but got: {data}"
        return

    with allure.step("Verify response contains 'data' as a list"):
        assert "data" in data
        assert isinstance(data["data"], list)

    with allure.step("Check number of facts returned matches expectations"):
        if limit is not None:
            assert (
                len(data["data"]) == limit
            ), f"Expected fact count to be {limit}, but got {len(data['data'])}. Parameters: {params_str}"
        else:
            assert (
                len(data["data"]) >= expected_data_count_min
            ), f"Expected at least {expected_data_count_min} fact(s), but got {len(data['data'])}. Parameters: {params_str}"

    with allure.step("Check structure and validity of each fact item"):
        for fact_item in data["data"]:
            assert "fact" in fact_item
            assert "length" in fact_item
            assert isinstance(fact_item["fact"], str)
            assert isinstance(fact_item["length"], int)

            assert len(fact_item["fact"]) == fact_item["length"], (
                f"Fact length mismatch: Expected {fact_item['length']}, "
                f"got {len(fact_item['fact'].strip())}. Fact: '{fact_item['fact']}'"
            )

            if max_length is not None:
                assert (
                    fact_item["length"] <= max_length
                ), f"Fact length {fact_item['length']} exceeds max_length {max_length}. Fact: '{fact_item['fact']}'"

    logging.info(f"Test {test_id} completed successfully.")
