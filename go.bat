"C:\Users\peter\Desktop\autoRPA\venv\Scripts\python.exe" "loginNotes.py"
if %errorlevel% neq 0 goto :end

"C:\Users\peter\Desktop\autoRPA\venv\Scripts\python.exe" "online.py"

:end
pause
