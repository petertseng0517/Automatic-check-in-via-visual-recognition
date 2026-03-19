# autoRPA — Lotus Notes 自動簽到機器人

利用電腦視覺與 GUI 自動化技術，每日自動完成 Lotus Notes 登入、健康調查與自動簽到流程，無須人工操作。

---

## 功能特色

- **自動登入** — 偵測密碼框出現後自動輸入密碼並送出
- **視覺辨識導航** — 以圖片比對定位 UI 元素，不依賴固定座標，螢幕解析度變動不影響穩定性
- **健康調查自動填答** — 一次找出畫面上所有「否」選項並批次點擊
- **請假日自動跳過** — 讀取 `leave.csv`，遇假日自動中止，不誤打卡
- **安全憑證管理** — 密碼存於 `.env`，不寫入程式碼或版本控制
- **無聲背景執行** — 透過 `run_hidden.vbs` 靜默啟動，不彈出黑色視窗

---

## 環境需求

| 項目 | 版本 |
|------|------|
| Windows | 10 / 11 |
| Python | 3.10 以上（建議 3.14） |
| Lotus Notes | 已安裝於本機 |

---

## 安裝步驟

**1. 建立虛擬環境並安裝套件**

```bash
python -m venv venv
venv\Scripts\activate
pip install pyautogui opencv-python pyscreeze python-dotenv
```

**2. 建立 `.env` 檔案（放在 `venv/` 目錄內）**

```
NOTES_PASSWORD=你的Lotus Notes密碼
LINE_TOKEN=（選填）LINE Notify 權杖
```

> `.env` 已加入 `.gitignore`，不會被推送至遠端。

**3. 確認 Lotus Notes 執行檔路徑**

開啟 `loginNotes.py`，確認以下路徑與本機相符：

```python
NOTES_PATH = r"C:\Program Files (x86)\Lotus\Notes\notes.exe"
```

---

## 使用方式

| 方式 | 說明 |
|------|------|
| `python loginNotes.py` | 直接執行（顯示輸出視窗） |
| 雙擊 `go.bat` | 透過虛擬環境執行 |
| 雙擊 `run_hidden.vbs` | 靜默背景執行，不顯示視窗 |

搭配 **Windows 工作排程器** 設定每日定時觸發 `run_hidden.vbs`，即可達成全自動排程簽到。

---

## 設定請假日

在 `leave.csv` 中，每行填入一個請假日期（格式：`YYYY/MM/DD`）：

```
2026/01/01
2026/02/28
```

程式啟動時若偵測到今日在名單內，會自動停止，不執行任何操作。

---

## 專案結構

```
autoRPA/
├── loginNotes.py            # 主程式（圖片辨識版）
├── coordinate_loginNotes.py # 舊版（固定座標版，參考用）
├── detect.py                # 滑鼠座標偵測工具
├── go.bat                   # 啟動批次檔
├── run_hidden.vbs           # 靜默啟動腳本
├── leave.csv                # 請假日期清單
├── check01.png              # UI 圖片：簽到資料庫圖示
├── check02.png              # UI 圖片：正式簽到按鈕
├── check03.png              # UI 圖片：健康調查「否」按鈕
├── password_box.png         # UI 圖片：密碼輸入框
├── submit_btn.png           # UI 圖片：送出按鈕
└── venv/                    # Python 虛擬環境（含 .env）
```

---

## 替換 UI 圖片

若 Lotus Notes 介面更新導致辨識失敗，請重新截圖替換對應 PNG 檔案：

1. 執行 `detect.py` 取得目標元素的螢幕座標
2. 使用截圖工具（如 Snipping Tool）截取目標按鈕／欄位
3. 覆蓋舊的 PNG 檔案，檔名保持不變

---

## 安全機制

- **Failsafe**：執行中將滑鼠移至螢幕左上角 (0, 0) 可立即中止程式
- **逾時保護**：每個步驟設有 10–60 秒逾時，避免無限等待
- **信心閾值**：圖片比對需達 80–85% 相似度才執行點擊，防止誤觸
