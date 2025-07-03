import requests
import pytest

BASE_URL = "https://catfact.ninja"

# TC_CF_001: 取得單一隨機貓咪事實
def test_get_single_cat_fact():
    """
    測試取得單一隨機貓咪事實。
    驗證狀態碼、JSON 結構及 fact 與 length 的一致性。
    """
    url = f"{BASE_URL}/fact"
    print(f"\n正在測試 URL: {url}")

    response = requests.get(url)
    print(f"回應狀態碼: {response.status_code}")
    print(f"回應主體: {response.text}")

    assert response.status_code == 200, \
        f"預期狀態碼為 200，但卻收到 {response.status_code}"

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        pytest.fail(f"回應不是有效的 JSON: {response.text}")

    # 驗證 JSON 結構和資料類型
    assert "fact" in data, "回應中應包含 'fact' 欄位"
    assert "length" in data, "回應中應包含 'length' 欄位"
    assert isinstance(data["fact"], str), "'fact' 欄位應為字串"
    assert isinstance(data["length"], int), "'length' 欄位應為整數"

    # 驗證 fact 的長度與 length 值一致 (去除首尾空白後)
    # 這裡應用 .strip() 來處理可能存在的首尾空白導致的長度不匹配問題
    assert len(data["fact"].strip()) == data["length"], \
        f"事實長度不匹配 (去除首尾空白後): 預期 {data['length']}，實際 {len(data['fact'].strip())}。原始事實: '{data['fact']}'"

# TC_CF_002, TC_CF_003, TC_CF_004, TC_CF_005: 取得多個貓咪事實 (含參數組合)
@pytest.mark.parametrize("limit, max_length, expected_data_count_min", [
    (None, None, 1), # TC_CF_002: 預設取得一個 (或更多，但至少一個)
    (3, None, 3),    # TC_CF_003: 取得指定數量 (limit=3)
    (None, 50, 1),   # TC_CF_004: 取得指定最大長度 (max_length=50)。由於 max_length 也會影響數量，此處 `expected_data_count_min` 仍設為1
    (2, 30, 2),      # TC_CF_005: 組合參數 (limit=2, max_length=30)
])
def test_get_multiple_cat_facts(limit, max_length, expected_data_count_min):
    """
    測試取得多個貓咪事實，並驗證 limit 和 max_length 參數。
    """
    url = f"{BASE_URL}/facts"
    params = {}
    if limit is not None:
        params["limit"] = limit
    if max_length is not None:
        params["max_length"] = max_length

    print(f"\n正在測試 URL: {url}, 參數: {params}")

    response = requests.get(url, params=params)
    print(f"回應狀態碼: {response.status_code}")
    print(f"回應主體: {response.text}")

    assert response.status_code == 200, \
        f"預期狀態碼為 200，但卻收到 {response.status_code}"

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        pytest.fail(f"回應不是有效的 JSON: {response.text}")

    # 驗證頂層 JSON 結構
    assert "data" in data, "回應中應包含 'data' 陣列"
    assert isinstance(data["data"], list), "'data' 欄位應為列表"

    # 驗證事實的數量 (針對 limit 參數)
    if limit is not None:
        assert len(data["data"]) == limit, \
            f"預期事實數量為 {limit}，實際為 {len(data['data'])}。參數: {params}"
    else: # 如果沒有指定 limit，通常會返回預設數量 (Cat Facts 預設為 1)
        assert len(data["data"]) >= expected_data_count_min, \
            f"預期至少 {expected_data_count_min} 個事實，實際為 {len(data['data'])}。參數: {params}"


    # 確保有事實可供驗證，尤其是在 limit=0 的情況下，這裡可能是空列表，但我們目前的用例預期有事實
    if len(data["data"]) == 0 and expected_data_count_min > 0:
        pytest.fail(f"事實列表為空，但預期至少有 {expected_data_count_min} 個事實。參數: {params}")

    for fact_item in data["data"]:
        assert "fact" in fact_item, "每個事實項目應包含 'fact' 欄位"
        assert "length" in fact_item, "每個事實項目應包含 'length' 欄位"
        assert isinstance(fact_item["fact"], str), "'fact' 欄位應為字串"
        assert isinstance(fact_item["length"], int), "'length' 欄位應為整數"

        # 驗證事實長度與 length 值一致 (去除首尾空白後)
        assert len(fact_item["fact"].strip()) == fact_item["length"], \
            f"事實長度不匹配 (去除首尾空白後): 預期 {fact_item['length']}，實際 {len(fact_item['fact'].strip())}。原始事實: '{fact_item['fact']}'"

        # 驗證事實長度是否符合 max_length (如果指定了)
        if max_length is not None:
            assert fact_item["length"] <= max_length, \
                f"事實長度 {fact_item['length']} 超過最大長度 {max_length}。事實: '{fact_item['fact']}'"