"""
recapture.py — 以 pyautogui 截圖為基準，裁切參考圖片

使用方式：
1. 先開啟 Lotus Notes / 線上系統，讓目標按鈕出現在螢幕上
2. 執行此腳本：python recapture.py
3. 選擇要更新的圖片（或全部截一張全螢幕）
4. 把游標移到目標左上角，按 S 記錄，再移到右下角，按 E 記錄，按 C 裁切儲存

快速鍵：
  S        — 記錄裁切起點（左上角）
  E        — 記錄裁切終點（右下角）
  C        — 執行裁切並儲存到指定檔名
  F        — 截一張全螢幕（screen_full.png），方便手動量座標
  Q / ESC  — 離開
"""

import sys
import time
import pyautogui
from PIL import Image
import keyboard  # pip install keyboard

pyautogui.FAILSAFE = True

TARGETS = [
    "password_box.png",
    "check.png",
    "no.png",
    "submit_btn.png",
    "login-online.png",
]

def take_full_screenshot(filename="screen_full.png"):
    print(f"📸 3 秒後截取全螢幕，請先切到目標視窗...")
    time.sleep(3)
    img = pyautogui.screenshot()
    img.save(filename)
    w, h = img.size
    print(f"✅ 已儲存 {filename}（{w} × {h} px，此為 pyautogui 實際看到的解析度）")
    return img

def crop_and_save(img, x1, y1, x2, y2, filename):
    left, top = min(x1, x2), min(y1, y2)
    right, bottom = max(x1, x2), max(y1, y2)
    if right <= left or bottom <= top:
        print("⚠️  無效範圍，請重選")
        return False
    cropped = img.crop((left, top, right, bottom))
    cropped.save(filename)
    cw, ch = cropped.size
    print(f"✅ 已儲存 {filename}（{cw} × {ch} px）")
    return True

def interactive_crop(img, filename):
    print(f"\n=== 裁切目標：{filename} ===")
    print("  把游標移到目標左上角，按 S 記錄起點")
    print("  把游標移到目標右下角，按 E 記錄終點")
    print("  按 C 裁切儲存，按 R 重選，按 Q 跳過此圖")

    start = None
    end = None

    while True:
        if keyboard.is_pressed('s'):
            start = pyautogui.position()
            print(f"  📌 起點：{start}")
            time.sleep(0.4)
        elif keyboard.is_pressed('e'):
            end = pyautogui.position()
            print(f"  📌 終點：{end}")
            time.sleep(0.4)
        elif keyboard.is_pressed('c'):
            if start and end:
                ok = crop_and_save(img, start.x, start.y, end.x, end.y, filename)
                if ok:
                    time.sleep(0.4)
                    return True
            else:
                print("  ⚠️  請先按 S 記錄起點、E 記錄終點")
            time.sleep(0.4)
        elif keyboard.is_pressed('r'):
            start = end = None
            print("  🔄 已重置，重新選擇")
            time.sleep(0.4)
        elif keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
            print(f"  ⏭  跳過 {filename}")
            time.sleep(0.4)
            return False
        time.sleep(0.05)

def main():
    print("=" * 55)
    print("  autoRPA 參考圖片重新截取工具")
    print("=" * 55)
    print("\n請選擇模式：")
    print("  1 — 截全螢幕（screen_full.png），再用影像編輯器手動量座標")
    print("  2 — 互動式裁切（用鍵盤 S/E/C 標記範圍）")
    print("  Q — 離開")

    choice = input("\n輸入選項：").strip().upper()

    if choice == "Q":
        return

    if choice == "1":
        take_full_screenshot()
        print("\n提示：開啟 screen_full.png，用 Windows 「相片」或 Paint 看像素座標，")
        print("      再修改程式裡的 region 參數，或改用座標直接點擊。")
        return

    if choice == "2":
        print("\n請選擇要更新哪些圖片：")
        for i, t in enumerate(TARGETS, 1):
            print(f"  {i} — {t}")
        print("  A — 全部")
        print("  Q — 離開")

        sel = input("\n輸入選項（多個用逗號分隔，例如 1,3）：").strip().upper()
        if sel == "Q":
            return

        if sel == "A":
            selected = TARGETS[:]
        else:
            indices = [s.strip() for s in sel.split(",")]
            selected = []
            for idx in indices:
                try:
                    selected.append(TARGETS[int(idx) - 1])
                except (ValueError, IndexError):
                    print(f"  ⚠️  無效選項 '{idx}'，跳過")

        if not selected:
            print("沒有選擇任何目標，結束。")
            return

        print(f"\n將依序截取：{selected}")
        print("請先把目標畫面切到前景，腳本會在 5 秒後截取全螢幕作為基準...\n")
        img = take_full_screenshot("screen_full.png")

        for filename in selected:
            interactive_crop(img, filename)

        print("\n✅ 完成！新的參考圖片已覆蓋舊檔。")
        print("   請重新執行 loginNotes.py 測試辨識效果。")

if __name__ == "__main__":
    try:
        import keyboard
    except ImportError:
        print("請先安裝 keyboard 套件：")
        print("  venv\\Scripts\\pip install keyboard")
        sys.exit(1)

    main()
