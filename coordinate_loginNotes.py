import pyautogui
import time

# 加上防呆機制：把滑鼠甩到螢幕最左上角(0,0)，程式就會強制停止！(非常重要)
pyautogui.FAILSAFE = True

print("RPA 腳本將在 3 秒後開始執行，請雙手離開鍵盤滑鼠...")
time.sleep(3)

# 1. 移動滑鼠到指定座標 (X=327, Y=2108)，花費 0.5 秒的時間滑過去（比較像真人）
pyautogui.moveTo(327, 2108, duration=0.5)

# 2. 點擊滑鼠左鍵
pyautogui.click()

# 3. 稍微等一下，確保游標已經在輸入框內
time.sleep(0.5)

# 4. 輸入英文字 (PyAutoGUI 預設不支援直接打中文，需搭配剪貼簿，這裡先用英文示範)
pyautogui.write('pass1234', interval=0.05) # interval 是每個字母的打字間隔

# 5. 按下 Enter 鍵
pyautogui.press('enter')



# 6. 移動滑鼠到指定座標-開啟簽到退 (X=390, Y=323)，花費 0.5 秒的時間滑過去（比較像真人）
pyautogui.moveTo(390, 323, duration=0.5)

# 7. 點擊滑鼠左鍵
pyautogui.doubleClick(interval=0.2)

# 8. 稍微等一下，確保簽到退化畫面已經開啟
time.sleep(0.5)


# 9. 移動滑鼠到指定座標-開啟簽到退 (X=320, Y=455)，花費 0.5 秒的時間滑過去（比較像真人）
pyautogui.moveTo(320, 455, duration=0.5)

# 10. 點擊滑鼠左鍵(點選正常簽到)
pyautogui.doubleClick(interval=0.2)

# 11. 稍微等一下，確保簽到退化畫面已經開啟
time.sleep(0.5)

# 12. 移動滑鼠到指定座標-開啟簽到退 (X=1328, Y=911)，花費 0.5 秒的時間滑過去（比較像真人）
pyautogui.moveTo(1328, 911, duration=0.5)

# 13. 點擊滑鼠左鍵
pyautogui.click()

# 15. 移動滑鼠到指定座標-開啟簽到退 (X=1965, Y=909)，花費 0.5 秒的時間滑過去（比較像真人）
pyautogui.moveTo(1965, 909, duration=0.5)

# 16. 點擊滑鼠左鍵
pyautogui.click()

# 15. 移動滑鼠到指定座標-開啟簽到退 (X=1965, Y=909)，花費 0.5 秒的時間滑過去（比較像真人）
pyautogui.moveTo(2564, 372, duration=0.5)


print("RPA 自動簽到任務完成！")