import os
import sys
import time
from datetime import datetime
import pyautogui
import pyscreeze
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
pyautogui.FAILSAFE = True

load_dotenv()

ONLINE_URL = "online.url"


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
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, grayscale=True)
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


if __name__ == "__main__":
    print("🚀 Online 登入腳本啟動...")

    # Step 1：開啟網頁
    print(f"🌐 開啟：{ONLINE_URL}")
    try:
        os.startfile(ONLINE_URL)
    except Exception as e:
        print(f"❌ 無法開啟 {ONLINE_URL}：{e}")
        sys.exit()
    time.sleep(5)

    # Step 2：點擊登入按鈕
    if not wait_and_click("login-online.png", timeout=30, confidence=0.85):
        print("❌ 找不到登入按鈕，程式結束。")
        sys.exit()
    print("✅ 已點擊登入按鈕！")

    # Step 3：傳送完成通知
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    notify_line(f"簽到順利完成，時間 {now}")
    print(f"📱 LINE 通知已送出")
