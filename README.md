# Setup

## Install dependencies 

1. Follow https://python-poetry.org/docs/ to install Poetry.
2. Run `poetry install`
3. Run `poetry shell`

## Setup env file
1. Add the env varibles from the template in `.env~` to your bash profile.
2. Visit Discord's developer platform to retrieve a bot token for `CORDIA_TOKEN`.

## Start local DB

1. Set `CORDIA_USER` and `CORDIA_PASSWORD` in your bash profile env.
2. Run `cd psql` and `docker compose up -d` to start a psql database.
3. Back in the projects root, run `alembic upgrade head` to run migrations

## Creating Migrations

1. Run `alembic revision -m "Revision change message"` to create a db migration
2. `alembec upgrade head` to migrate to lastest.
3. `alembic downgrade base` to downgrade to oldest.

## Running the bot
1. Ensure you are in a venv (`poetry shell`)
2. Run `python3 main.py`
