# ebook-reader-backend

## Setup

- `pip install -r requirements.txt`
- get the .env file
- setup a db with the name you set in the .env file
- `python manage.py migrate`

## Code Formatting

- `black` is used as a code formatter, have it set in your VSCode Settings.
- After `pip install -r requirements.txt`, go to `Preferences -> Settings -> Python Formatting Provider -> Select black`.
- Also enable `Format on Save`.
