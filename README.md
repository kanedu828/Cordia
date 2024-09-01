# Setup

## Install dependencies 

1. Follow https://python-poetry.org/docs/ to install Poetry.
2. Run `poetry install`
3. Run `poetry shell`

## Setup env file
1. Create a `.env` file and follow the template in `.env~`.
2. Visit Discord's developer platform to retrieve a bot token for `CORDIA_TOKEN`.

## Start local DB

1. Set `CORDIA_USER` and `CORDIA_PASSWORD` in your bash profile env.
2. Run `cd psql` and `docker compose up -d` to start a psql database.
3. Back in the projects root, run `alembic upgrade head` to run migrations

## Creating Migrations

1. Run `alembic revision -m "Revision change message"` to create a db migration
