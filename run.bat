@echo off
if not exist venv (
  python -m venv venv
  venv\Scripts\activate
  pip install --upgrade pip
  pip install -r requirements.txt
)
venv\Scripts\activate
python app.py
pause
