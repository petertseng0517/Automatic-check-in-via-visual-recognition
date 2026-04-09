@echo off
:: 切換到檔案所在的目錄 ( %~dp0 代表 .bat 檔案所在的資料夾)
cd /d "%~dp0"



"C:\Users\peter\Desktop\autoRPA\venv\Scripts\python.exe" "online.py"

:end
pause
