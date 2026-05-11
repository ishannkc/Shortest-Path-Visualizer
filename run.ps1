Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

& "$PSScriptRoot\.venv\Scripts\python.exe" "$PSScriptRoot\backend\app.py"
