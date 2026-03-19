import pyautogui
import time

print("按下 Ctrl-C 可以中斷程式。")
try:
    while True:
        # 取得目前滑鼠座標
        x, y = pyautogui.position()
        positionStr = f'X: {str(x).rjust(4)} Y: {str(y).rjust(4)}'
        
        # 印出座標並清除上一行（讓畫面乾淨）
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print('\n已結束偵測。')