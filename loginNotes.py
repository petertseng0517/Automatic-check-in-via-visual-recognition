import os
import sys
import csv
import subprocess
from datetime import datetime
import pyautogui
import time
import pyscreeze
import requests
from dotenv import load_dotenv

pyautogui.FAILSAFE = True

load_dotenv()

# ==========================================
# 設定
# ==========================================
CHECKIN_URL = "checkin.url"
LEAVE_CSV_PATH = "leave.csv"
YOUR_PASSWORD = os.getenv("NOTES_PASSWORD")

if not YOUR_PASSWORD:
    print("❌ 錯誤：找不到密碼，請檢查 .env 檔案是否設定正確！")
    sys.exit()
# ==========================================


def notify_line(message):
    """透過 LINE Messaging API 傳送通知訊息。"""
    token = os.getenv("LINE_CHANNEL_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    if not token or not user_id:
        return
    try:
        requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "to": user_id,
                "messages": [{"type": "text", "text": message}]
            },
            timeout=10,
            verify=False
        )
    except Exception:
        pass


def wait_and_click(image_path, timeout=60, confidence=0.85):
    """持續尋找畫面上的單一目標圖片，找到就點擊。"""
    print(f"👀 尋找：{image_path} ...")
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            print(f"⏳ 失敗：等了 {timeout} 秒都沒看到 {image_path}，放棄執行！")
            return False

        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location is not None:
                print(f"🎯 找到了！座標：{location}")
                time.sleep(0.5)
                pyautogui.moveTo(location, duration=0.3)
                pyautogui.click()
                return True
        except (pyautogui.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            pass
        except Exception:
            pass

        time.sleep(0.5)


def wait_and_click_all(image_path, timeout=60, confidence=0.85):
    """持續尋找畫面上所有符合的目標圖片，逐一點擊。"""
    print(f"👀 尋找所有：{image_path} ...")
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            print(f"⏳ 失敗：超時放棄尋找所有 {image_path}。")
            return False

        try:
            all_locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))

            if all_locations:
                print(f"🎯 找到 {len(all_locations)} 個目標，準備批次點擊...")
                time.sleep(0.5)

                for loc in all_locations:
                    center_point = pyautogui.center(loc)
                    print(f"👉 點擊座標：{center_point}")
                    pyautogui.moveTo(center_point, duration=0.3)
                    pyautogui.click()
                    time.sleep(0.3)

                return True
        except (pyautogui.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            pass
        except Exception:
            pass

        time.sleep(0.5)


# ==========================================
# 主程式
# ==========================================
if __name__ == "__main__":
    print("🚀 RPA 自動簽到腳本啟動...")

    # 請假日檢查
    today_str = datetime.now().strftime("%Y/%m/%d")
    print(f"📅 檢查今日 ({today_str}) 是否為請假日...")
    try:
        with open(LEAVE_CSV_PATH, mode='r', encoding='utf-8-sig') as file:
            for row in csv.reader(file):
                if row and row[0].strip() == today_str:
                    print(f"🛑 今日 ({today_str}) 在請假名單中，自動停止執行。")
                    sys.exit()
        print("✅ 今日無請假紀錄，開始執行自動化流程...")
    except FileNotFoundError:
        print(f"⚠️ 找不到 {LEAVE_CSV_PATH}，預設為正常上班日。")

    # Step 1：開啟簽到表單
    print(f"🌐 開啟簽到表單：{CHECKIN_URL}")
    try:
        os.startfile(CHECKIN_URL)
    except Exception as e:
        print(f"❌ 無法開啟 {CHECKIN_URL}：{e}")
        sys.exit(1)
    time.sleep(5)

    # Step 2：輸入密碼
    if not wait_and_click("password_box.png", timeout=60, confidence=0.85):
        print("❌ 找不到密碼輸入框，程式結束。")
        notify_line("❌ 簽到失敗：找不到密碼輸入框")
        sys.exit(1)
    print("🔑 輸入密碼...")
    pyautogui.write(YOUR_PASSWORD, interval=0.05)
    pyautogui.press('enter')
    time.sleep(3)

    # Step 3：點擊正常簽到
    if not wait_and_click("check.png", timeout=30, confidence=0.85):
        print("❌ 找不到正常簽到按鈕，程式結束。")
        notify_line("❌ 簽到失敗：找不到正常簽到按鈕")
        sys.exit(1)
    print("✅ 已點擊正常簽到！")
    time.sleep(2)

    # Step 4：點選所有「否」
    if not wait_and_click_all("no.png", timeout=30, confidence=0.90):
        print("❌ 找不到健康調查表的否選項，程式結束。")
        notify_line("❌ 簽到失敗：找不到健康調查否選項")
        sys.exit(1)
    print("✅ 所有「否」已點選完畢！")
    time.sleep(1)

    # Step 4.5：Step 4 完成後執行 online.py
    print("🌐 Step 4 完成，開始執行 online.py...")
    try:
        subprocess.run([sys.executable, "online.py"], check=True)
        print("✅ online.py 執行完成。")
    except subprocess.CalledProcessError as e:
        print(f"❌ online.py 執行失敗，錯誤碼：{e.returncode}")
        notify_line("❌ 簽到失敗：online.py 執行失敗")
        sys.exit(1)

    # Step 5：點擊確定送出
    if not wait_and_click("submit_btn.png", timeout=10, confidence=0.85):
        print("❌ 找不到確定按鈕，程式結束。")
        notify_line("❌ 簽到失敗：找不到確定按鈕")
        sys.exit(1)
    print("🎉 自動簽到完成！")
    notify_line("✅ 自動簽到完成！")