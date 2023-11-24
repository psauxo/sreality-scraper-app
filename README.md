# Simple HTTP server with Scrapy

This is a simple HTTP server that uses Scrapy to crawl a website (sreality.cz) via sreality_spider.py and save results in db.

# Common requirements:

## Setup environment variables

```bash
$ cp .env.example .env
$ vi .env
```

# To run locally:

## Installation

```bash
$ poetry install
$ source .venv/bin/activate
```

## Setup PYTHONPATH

```bash
$ export PYTHONPATH=$PYTHONPATH:$(pwd)
$ echo $PYTHONPATH
```

## Run the server

```bash
$ python http_server/server.py
```

## Run the scraper spider (in another terminal)

```bash
$ scrapy runspider scraper/spiders/sreality_spider.py
```

# To run with docker-compose:

## Run docker-compose in detached mode

```bash
$ docker-compose up -d
```

## Run tests

```bash
$ docker exec -it sreality_scraper_app pytest
```

## Project structure

```bash
├── README.md
├── app
│   ├── __init__.py
│   ├── controller.py
│   ├── services
│   │   ├── __init__.py
│   │   └── html_generator.py
│   └── views.py
├── database
│   ├── __init__.py
│   ├── apply_migrations.py
│   ├── config.py
│   ├── factory.py
│   ├── migrations
│   │   ├── README
│   │   ├── __init__.py
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── 7aa62226dcd8_initial_migration.py
│   │       ├── __init__.py
│   ├── services
│   │   ├── base.py
│   │   ├── flat.py
│   │   └── pagination.py
│   └── sql_schema.py
├── docker
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── init_db.sh
├── docker-compose.yml
├── http_server
│   ├── __init__.py
│   ├── config.py
│   ├── handler.py
│   ├── main.py
│   ├── router.py
│   └── server.py
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── scraper
│   ├── __init__.py
│   ├── constants.py
│   ├── error_handler.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── scrapy.cfg
│   ├── services
│   │   ├── __init__.py
│   │   ├── configuration.py
│   │   ├── extractor.py
│   │   ├── parser.py
│   │   └── schema.py
│   ├── settings.py
│   └── spiders
│       ├── __init__.py
│       └── sreality_spider.py
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── test_app
    │   ├── __init__.py
    │   ├── test_html_generator.py
    │   └── test_view.py
    ├── test_http_server
    │   ├── __init__.py
    │   └── test_server.py
    ├── test_scraper
    │   ├── __init__.py
    │   ├── test_services
    │   │   ├── test_api_response_parser.py
    │   │   └── test_json_data_extractor.py
    │   └── test_spider.py
    └── utils.py
```
