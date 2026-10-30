@echo off
IF NOT EXIST venv (
    echo Creating venv...
    python -m venv venv
)
call venv\Scripts\activate
pip install mysql-connector-python
python main.py
