# Sliding Window Algorithm

1. This app was created on Windows 11, with Python 3.9.12

2. The Python program "app.py" implements the Sliding Window algorithm (which is a rate-limiting technique) at the backend.

3. The Python program "test_script.py" tests it, by forking 4 processes which parallely access the backend.
- Reference: line 27 (of "test_script.py")

4. The PowerShell script "module.ps1" downloads the necessary modules, i.e., 'flask' & 'requests', if these aren't installed already.
- The versions are specified within it.

5. The PowerShell script "run.ps1" creates two shells to run "app.py" & "test_script.py"
