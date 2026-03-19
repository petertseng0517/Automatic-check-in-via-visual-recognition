import os
import sys
import csv
from datetime import datetime
import pyautogui
import time
import subprocess
import pyscreeze
from dotenv import load_dotenv

# 載入 .env 檔案裡面的環境變數
load_dotenv()

# ==========================================
# 請在這裡填寫你的專屬設定
# ==========================================
NOTES_PATH = r"C:\Program Files (x86)\Lotus\Notes\notes.exe" 
PASSWORD_IMAGE = "password_box.png"  
LEAVE_CSV_PATH = "leave.csv"

# 👇 改從 .env 檔案中安全讀取機密資料 👇
YOUR_PASSWORD = os.getenv("NOTES_PASSWORD") 
LINE_TOKEN = os.getenv("LINE_TOKEN")

# 防呆檢查：如果忘記建 .env 或變數名稱打錯，程式會提早報錯
if not YOUR_PASSWORD:
    print("❌ 錯誤：找不到密碼，請檢查 .env 檔案是否設定正確！")
    sys.exit()

# ==========================================

def wait_and_click(image_path, timeout=60, confidence=0.85, is_double_click=False):
    """
    智慧等待機制：不斷尋找畫面上的「單一」目標圖片，找到就點擊。
    """
    print(f"👀 開始監測畫面，尋找：{image_path} ...")
    start_time = time.time()
    
    while True:
        if time.time() - start_time > timeout:
            print(f"⏳ 失敗：等了 {timeout} 秒都沒看到畫面，放棄執行！")
            return False
        
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location is not None:
                print(f"🎯 找到了！目標座標在 {location}")
                time.sleep(0.5)
                pyautogui.moveTo(location, duration=0.3)
                
                if is_double_click:
                    pyautogui.click()      
                    time.sleep(0.5)        
                    pyautogui.press('enter') 
                else:
                    pyautogui.click()
                
                return True
                
        except (pyautogui.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            pass
        except Exception as e:
            pass
        
        time.sleep(0.5)

def wait_and_click_all(image_path, timeout=60, confidence=0.85):
    """
    智慧等待機制：尋找畫面上「所有」符合圖片的目標，並一個一個點擊。
    """
    print(f"👀 開始監測畫面，準備尋找畫面上所有：{image_path} ...")
    start_time = time.time()
    
    while True:
        if time.time() - start_time > timeout:
            print(f"⏳ 失敗：超時放棄尋找所有目標。")
            return False
        
        try:
            all_locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            
            if all_locations:
                print(f"🎯 🎯 找到了！畫面上共有 {len(all_locations)} 個目標。準備批次點擊...")
                time.sleep(0.5)
                
                for loc in all_locations:
                    center_point = pyautogui.center(loc)
                    print(f"👉 正在點擊目標，座標: {center_point}")
                    pyautogui.moveTo(center_point, duration=0.3)
                    pyautogui.click()
                    time.sleep(0.3) 
                
                return True
                
        except (pyautogui.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            pass
        except Exception as e:
            pass
            
        time.sleep(0.5)

# ==========================================
# 主程式執行區
# ==========================================
if __name__ == "__main__":
    print("🚀 RPA 登入腳本啟動...")

    # 👇👇👇 正確加入的請假防呆機制 👇👇👇
    today_str = datetime.now().strftime("%Y/%m/%d") 
    print(f"📅 正在檢查今日 ({today_str}) 是否為請假日...")
    
    try:
        with open(LEAVE_CSV_PATH, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip() == today_str:
                    print(f"🛑 發現今日 ({today_str}) 在請假名單中！機器人將自動停止執行，祝您好好休息！")
                    sys.exit() # 發現請假，程式直接在這裡結束
        print("✅ 今日無請假紀錄，準備開始執行自動化流程...")
    except FileNotFoundError:
        print(f"⚠️ 找不到請假檔案 ({LEAVE_CSV_PATH})，預設為正常上班日。")
    # 👆👆👆 防呆機制結束 👆👆👆

    print(f"正在啟動 Lotus Notes: {NOTES_PATH}")
    try:
        subprocess.Popen(NOTES_PATH)
    except FileNotFoundError:
        print("❌ 找不到 Lotus Notes 執行檔，請檢查 NOTES_PATH 路徑是否正確。")
        sys.exit()

    if wait_and_click(PASSWORD_IMAGE, timeout=60, confidence=0.85):
        print("🔑 準備輸入密碼...")
        pyautogui.write(YOUR_PASSWORD, interval=0.05)
        pyautogui.press('enter')
        print("✅ 登入動作完成！")
        
        time.sleep(3) 
        print("⏳ 等待 Notes 載入工作區畫面...")
        
        if wait_and_click("check01.png", timeout=30, confidence=0.85, is_double_click=True):
            print("✅ 成功點選並進入簽到資料庫！")
            
            if wait_and_click("check02.png", timeout=30, confidence=0.85):
                print("✅ 成功點選正式簽到！")
                
                print("⏳ 等待健康調查表畫面載入...")
                time.sleep(2) 
                
                if wait_and_click_all("check03.png", timeout=30, confidence=0.8):
                    print("✅ ✅ 成功點選所有「否」！自動簽到流程圓滿達成！")
                    
                    print("⏳ 準備點選最後的送出按鈕...")
                    time.sleep(1) 
                    if wait_and_click("submit_btn.png", timeout=10, confidence=0.85):
                        print("🎉 完美收工！自動簽到與健康調查表已徹底完成！")
                    else:
                        print("❌ 找不到最後的送出按鈕。")
                else:
                    print("❌ 找不到健康調查表的選項。")

            else:
                print("❌ 找不到正式簽到圖示。")

        else:
            print("❌ 找不到簽到系統圖示。")

    else:
        print("❌ 登入失敗：Lotus Notes 沒有正常開啟或找不到密碼框。")