# Run the first Python program in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command python app.py"

# Run the second Python program in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command python test_script.py"
