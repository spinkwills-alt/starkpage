' StartServer.vbs - Run server without console window
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d C:\Users\User\Desktop\stark && python server.py", 0, False
WshShell.Popup "Stark Expo Server started in background!", 3, "Server Started", 64