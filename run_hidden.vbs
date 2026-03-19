Set WshShell = CreateObject("WScript.Shell")
' 這裡的路徑請換成你 bat 檔的絕對路徑
WshShell.Run chr(34) & "C:\Users\peter\Desktop\autoRPA\go.bat" & Chr(34), 0
Set WshShell = Nothing