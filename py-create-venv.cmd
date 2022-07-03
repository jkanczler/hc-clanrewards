:: Creating the Python virtual environment
python -m venv .venv

:: Activating the virtual environment
CALL ./.venv/Scripts/activate

:: Intalling Python modules using the requirements.txt
python -m pip install -r requirements.txt
