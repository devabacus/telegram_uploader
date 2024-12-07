python -m venv env
.\env\Scripts\Activate.ps1

pip install python-telegram-bot

python -m pip freeze > requirements.txt
pip install pytest
