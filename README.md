# Cat Facts API 主要流程自動化測試

此儲存庫包含針對 [Cat Facts API](https://catfact.ninja) 主要流程的自動化測試。

## 目標 API

這些測試針對 Cat Facts API，其基本 URL 為 `https://catfact.ninja`。

## 測試案例

以下是實施的五個核心測試案例，涵蓋了 Cat Facts API 的主要功能，且預期會成功通過：

| 測試案例 ID | 情境                               | 請求方法 & 端點            | 參數 (如有)                        | 預期結果                                                                 | 驗證方法                                                                |
| :---------- | :--------------------------------- | :----------------------- | :--------------------------------- | :----------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| TC_CF_001   | **[主流程]** 取得單一隨機貓咪事實    | `GET /fact`              | 無                                 | 1. HTTP 狀態碼 200 (OK) <br> 2. 回應為 JSON 物件 <br> 3. 包含 `fact` (字串) 和 `length` (整數) 欄位 | 1. 檢查狀態碼 <br> 2. 檢查回應 JSON 結構和資料類型 <br> 3. 驗證 `fact` 長度與 `length` 值一致 |
| TC_CF_002   | **[主流程]** 取得多個貓咪事實 (預設數量) | `GET /facts`             | 無                                 | 1. HTTP 狀態碼 200 (OK) <br> 2. 回應為 JSON 物件 <br> 3. 包含 `data` (陣列) 欄位，且每個元素包含 `fact` 和 `length` | 1. 檢查狀態碼 <br> 2. 檢查回應 JSON 結構 <br> 3. 驗證 `data` 陣列的元素結構 |
| TC_CF_003   | **[主流程]** 取得指定數量的貓咪事實  | `GET /facts`             | `limit=3`                          | 1. HTTP 狀態碼 200 (OK) <br> 2. 回應為 JSON 物件 <br> 3. `data` 陣列的長度等於 `limit` | 1. 檢查狀態碼 <br> 2. 驗證 `data` 陣列的長度是否與 `limit` 相符 |
| TC_CF_004   | **[主流程]** 取得指定最大長度的貓咪事實 | `GET /facts`             | `max_length=50`                    | 1. HTTP 狀態碼 200 (OK) <br> 2. 回應為 JSON 物件 <br> 3. `data` 陣列中每個 `fact` 的長度 <= `max_length` | 1. 檢查狀態碼 <br> 2. 驗證每個 `fact` 的長度                               |
| TC_CF_005   | **[主流程]** 取得多個貓咪事實 (組合參數) | `GET /facts`             | `limit=2&max_length=30`            | 1. HTTP 狀態碼 200 (OK) <br> 2. 回應為 JSON 物件 <br> 3. `data` 陣列長度等於 `limit` <br> 4. 每個 `fact` 長度 <= `max_length` | 1. 檢查狀態碼 <br> 2. 驗證 `data` 陣列長度及每個 `fact` 長度             |

## 所使用的驗證

這些測試中使用的驗證方法主要集中在 API 的 HTTP 回應上：

* **HTTP 狀態碼驗證：** 驗證伺服器是否回應正確的 HTTP 狀態碼（例如，200 表示成功）。這確認了請求的基本結果。
* **JSON Schema 和資料類型驗證：** 當 API 返回 JSON 資料時，驗證 JSON 負載的結構非常重要。這包括：
    * 確保存在預期的欄位（例如 `fact`, `length`, `data`）。
    * 驗證這些欄位的資料類型是否正確（例如 `fact` 是字串，`length` 是整數，`data` 是陣列）。
    * 確認回應是物件或陣列，並且其內部結構符合預期。
* **資料內容驗證：** 針對 Cat Facts API 的特定參數，我們進行了額外的內容驗證：
    * **長度一致性：** 驗證返回的 `fact` 字串的實際長度是否與 `length` 欄位的值完全一致。
    * **最大長度限制：** 當使用 `max_length` 參數時，驗證所有返回的 `fact` 內容的長度都不超過該值。
    * **數量準確性：** 當使用 `limit` 參數時，驗證返回的 `data` 陣列中的事實數量是否與 `limit` 值完全匹配。

這些驗證共同確保 API 在正常情況下都按預期運行，提供可靠且符合參數要求的回應。

## 設定和執行測試

1.  **克隆儲存庫：**
    ```bash
    git clone [https://github.com/your-username/your-catfacts-tests-main-flow.git](https://github.com/your-username/your-catfacts-tests-main-flow.git)
    cd your-catfacts-tests-main-flow
    ```
2.  **創建虛擬環境（推薦）：**
    ```bash
    python -m venv venv
    source venv/bin/activate  # 在 Windows 上使用 `venv\Scripts\activate`
    ```
3.  **安裝依賴：**
    ```bash
    pip install pytest requests
    ```
4.  **運行測試：**
    ```bash
    pytest -v tests/test_cat_facts_api_main_flow.py
    ```

## 建議

* **Pytest parametrize:** 已在 `test_get_multiple_cat_facts` 測試函數中應用 `pytest.mark.parametrize`，以有效率地測試帶有不同參數組合的 `GET /facts` 端點。
* **可擴展性：** 這些測試案例提供了主流程的堅實基礎。未來可以根據需要增加更多負向測試（例如，傳入非整數的 `limit` 或 `max_length`）、邊界值測試（例如，`limit=0`、極大的 `limit` 或 `max_length`），以提高測試覆蓋率。
* **CI/CD 整合：** 考慮將此測試套件整合到持續整合/持續部署 (CI/CD) 流程中，以確保每次程式碼變更都能自動運行測試。