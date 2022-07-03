@IF EXIST "%~dp0\.venv\Scripts\python.exe" (
    "%~dp0\.venv\Scripts\python.exe" "%~dp0/src/__init__.py" %*
) ELSE (
    echo Failed to load python executable.
    exit /b 1
)