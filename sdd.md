# 規格驅動開發文件（SDD）
# autoRPA — Lotus Notes 自動簽到機器人

**版本**：v2.0  
**日期**：2026-04-03  
**作者**：petertseng0517  
**狀態**：正式

---

## 1. 專案背景

本專案（autoRPA）是一套用 Python 撰寫的桌面 RPA（機器人流程自動化）腳本，透過電腦視覺辨識技術自動完成每日 Lotus Notes 的登入、正常簽到，以及健康調查表填寫。

本文件（v2.0）依據使用者調整後的執行流程重新撰寫，主要變更為：以 `checkin.url` 捷徑直接開啟簽到表單，省略手動導航步驟；並更新模板圖檔（`check.png`、`no.png`）以提升視覺辨識準確率。

---

## 2. 問題描述（v1.0 遺留問題）

舊版流程使用 `check03.png` 作為健康調查表「否」按鈕的模板，因模板尺寸過小（0.8 KB）且 `locateAllOnScreen()` 掃描整個螢幕，導致偶發性誤點到畫面上其他視覺相似的按鈕（如簽退按鈕）。

v2.0 透過以下改善消除此問題：
1. 流程簡化（直接開啟表單，畫面干擾元素減少）
2. 更換模板圖檔（`no.png` 含有更多 UI 脈絡）

---

## 3. 執行流程規格

### 3.1 流程總覽

```
開啟 checkin.url（直接進入 Lotus Notes 簽到表單）
    ↓ 等待系統反應
找到密碼框（password_box.png）→ 輸入密碼 → 按 Enter
    ↓ 等待系統反應
找到正常簽到按鈕（check.png）→ 點擊
    ↓ 等待系統反應
找到所有否選項（no.png）→ 批次點擊每一個
    ↓ 等待系統反應
找到確定按鈕（submit_btn.png）→ 點擊 → 完成
```

### 3.2 各步驟規格

#### Step 1：開啟簽到表單

| 項目 | 規格 |
|------|------|
| 執行方式 | `os.startfile("checkin.url")` 或 `subprocess.Popen(["cmd", "/c", "start", "checkin.url"])` |
| 檔案 | `checkin.url`（內含 `notes://hladmin2/482570E40037E99B`） |
| 等待時間 | 執行後 `sleep(5)` 等待 Lotus Notes 開啟並載入表單 |
| 失敗處理 | 若檔案不存在，印出錯誤訊息並結束程式 |

> **說明**：直接以 URL 捷徑開啟，Lotus Notes 會跳過主介面、直接進入指定的簽到資料庫，避免舊流程需手動導航的問題。

#### Step 2：輸入密碼

| 項目 | 規格 |
|------|------|
| 模板圖檔 | `password_box.png` |
| 模板內容 | 「密碼(P):」標籤與輸入框 |
| confidence | `0.85` |
| timeout | `60` 秒 |
| 動作 | 找到後點擊輸入框，輸入密碼，按 Enter |
| 等待時間 | 按 Enter 後 `sleep(3)` 等待登入完成 |

#### Step 3：點擊正常簽到

| 項目 | 規格 |
|------|------|
| 模板圖檔 | `check.png` |
| 模板內容 | 藍框「正常簽到」按鈕 |
| confidence | `0.85` |
| timeout | `30` 秒 |
| 動作 | 找到後單擊 |
| 等待時間 | 點擊後 `sleep(2)` 等待健康調查表載入 |

#### Step 4：點選所有「否」

| 項目 | 規格 |
|------|------|
| 模板圖檔 | `no.png` |
| 模板內容 | 含圓圈選項與「否」字的核取按鈕 |
| confidence | `0.90` |
| timeout | `30` 秒 |
| 搜尋方式 | `locateAllOnScreen`（尋找畫面上所有符合目標） |
| 動作 | 逐一點擊每個找到的「否」按鈕 |
| 點擊間隔 | 每次點擊後 `sleep(0.3)` |
| 等待時間 | 全部點完後 `sleep(1)` |

#### Step 5：點擊確定送出

| 項目 | 規格 |
|------|------|
| 模板圖檔 | `submit_btn.png` |
| 模板內容 | 「確定」按鈕 |
| confidence | `0.85` |
| timeout | `10` 秒 |
| 動作 | 找到後單擊 |
| 完成 | 印出成功訊息，程式結束 |

---

## 4. 模板圖檔清單

| 檔案 | 用途 | 模板內容說明 | confidence |
|------|------|------------|-----------|
| `checkin.url` | 啟動捷徑 | Lotus Notes URL 捷徑（非圖片） | — |
| `password_box.png` | 密碼輸入框 | 含「密碼(P):」標籤與空白輸入框 | 0.85 |
| `check.png` | 正常簽到按鈕 | 藍框文字「正常簽到」 | 0.85 |
| `no.png` | 健康調查否按鈕 | 小圓圈 + 「否」字，含周圍留白 | 0.90 |
| `submit_btn.png` | 送出確定按鈕 | 框線 + 「確定」文字 | 0.85 |

---

## 5. 程式架構規格

### 5.1 核心函式

#### `wait_and_click(image_path, timeout, confidence)`
- 持續搜尋單一目標圖片，找到後點擊
- 超時回傳 `False`，找到並點擊回傳 `True`
- 每次輪詢間隔：`sleep(0.5)`

#### `wait_and_click_all(image_path, timeout, confidence)`
- 持續搜尋所有符合的目標圖片，找到後逐一點擊
- 超時回傳 `False`，完成回傳 `True`
- 每次點擊間隔：`sleep(0.3)`

### 5.2 主程式執行順序

```python
# 1. 讀取設定
load_dotenv()
YOUR_PASSWORD = os.getenv("NOTES_PASSWORD")

# 2. 請假日檢查（有請假則結束）
check_leave_csv()

# 3. 開啟 Lotus Notes 簽到表單
os.startfile("checkin.url")
time.sleep(5)

# 4. 輸入密碼
wait_and_click("password_box.png", timeout=60, confidence=0.85)
pyautogui.write(YOUR_PASSWORD, interval=0.05)
pyautogui.press('enter')
time.sleep(3)

# 5. 點擊正常簽到
wait_and_click("check.png", timeout=30, confidence=0.85)
time.sleep(2)

# 6. 點選所有否
wait_and_click_all("no.png", timeout=30, confidence=0.90)
time.sleep(1)

# 7. 點擊確定送出
wait_and_click("submit_btn.png", timeout=10, confidence=0.85)
```

### 5.3 安全機制

| 機制 | 說明 |
|------|------|
| `pyautogui.FAILSAFE = True` | 移動滑鼠至螢幕左上角 (0,0) 可強制終止程式 |
| timeout 超時保護 | 每個步驟均設定等待上限，避免無限等待 |
| 請假 CSV 檢查 | 若今日在 `leave.csv` 中，程式自動停止 |
| `.env` 密碼保護 | 密碼不寫死於程式碼，從環境變數讀取 |

---

## 6. 設定檔規格

### 6.1 `.env` 檔案

```env
NOTES_PASSWORD=pass1234
LINE_TOKEN=（選填，用於未來 LINE 通知）
```

### 6.2 `leave.csv` 格式

```
2026/01/01
2026/02/28
```
每行一個請假日期，格式 `YYYY/MM/DD`。

---

## 7. 測試計畫

| # | 測試項目 | 測試方式 | 預期結果 |
|---|---------|---------|---------|
| T1 | URL 捷徑開啟 | 手動點擊 `checkin.url` | Lotus Notes 直接進入簽到表單，不經過主介面 |
| T2 | 密碼框辨識 | 執行腳本，觀察是否正確找到密碼框 | 密碼自動輸入，成功登入 |
| T3 | 簽到按鈕辨識 | 觀察 `check.png` 是否正確定位 | 點擊「正常簽到」，畫面切換至健康調查表 |
| T4 | 否按鈕批次點擊 | 觀察所有「否」是否均被點選 | 所有題目均選「否」，無誤點其他元素 |
| T5 | 送出確認 | 觀察最後是否成功點擊確定 | 表單送出，流程完整結束 |
| T6 | 三日迴歸測試 | 連續三個工作日自動執行 | 每日均正常完成，無異常 |

---

## 8. 模板維護指南

### 8.1 何時需要更新模板圖檔

| 情境 | 需更新的圖檔 |
|------|------------|
| Lotus Notes UI 更新，按鈕外觀改變 | 對應的 PNG 圖檔 |
| 更換螢幕或變更解析度（DPI 不同） | 所有 PNG 圖檔 |
| 辨識率下降（常常 timeout） | 重新截圖對應圖檔 |

### 8.2 截圖原則

- 截圖時 Lotus Notes 視窗須處於**正常顯示狀態**（非最大化/最小化）
- 模板需包含按鈕本身及**四周至少 10px 的留白**
- 截圖後確認圖檔能在正常執行時被正確辨識再取代舊檔

### 8.3 工具

使用 `detect.py`（現有工具）可即時查看滑鼠座標，輔助確認辨識位置是否正確。

---

## 9. 部署方式

| 方式 | 指令/操作 | 適用場景 |
|------|---------|---------|
| 直接執行 | `python loginNotes.py` | 開發測試 |
| 批次檔執行 | 雙擊 `go.bat` | 手動觸發（顯示視窗） |
| 靜默執行 | 雙擊 `run_hidden.vbs` | 背景執行（無視窗） |
| 排程執行 | Windows 工作排程器呼叫 `run_hidden.vbs` | 每日自動執行 |

---

## 10. 已知限制與未來規劃

| 項目 | 說明 |
|------|------|
| 多顯示器環境 | `locateAllOnScreen` 通常僅掃描主螢幕，次螢幕的元素不會被誤抓，但同時也不會是目標。若視窗在次螢幕，需確認 pyautogui 設定 |
| 網路延遲 | Lotus Notes 開啟速度受網路影響，若公司 VPN 較慢，可視情況增加 Step 1 的 `sleep` 時間 |
| LINE 通知 | `.env` 已預留 `LINE_TOKEN`，未來可於流程失敗時推播通知（目前尚未實作） |

---

*本文件依據使用者 2026-04-03 調整的執行流程規格撰寫，取代 v1.0 版本。*
