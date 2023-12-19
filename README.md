# Project Brief

## Objective

The primary objective of this project is to develop a system that utilizes the Scrapy framework to scrape the first 500 items (including their titles and image URLs) from the real estate website sreality.cz, specifically focusing on flats for sale. These items should be saved in a PostgreSQL database. Additionally, the project involves implementing a simple HTTP server in Python, which will display these 500 items on a basic web page, showing each item's title and image.

---

### Key Requirements

- **Scraping**: Use Scrapy to scrape the first 500 items (titles and image URLs) from the 'flats for sale' section on sreality.cz.
- **Database**: Save the scraped data in a PostgreSQL database.
- **HTTP Server**: Create a simple Python-based HTTP server to display the scraped items on a web page.
- **Docker Integration**: Package the entire system using Docker, enabling it to be run with a single docker-compose up command.

### Execution

The system should be set up in such a way that executing `docker-compose up` will launch the entire application. Once running, the user can view the scraped advertisements by navigating to http://127.0.0.1:8080.

---

## HTTP Server

- Description: A minimalistic HTTP server, deliberately built without frameworks like Flask.
- Functionality: Displays 500 apartments for sale from sreality.cz at the route '/'.

## Scraper Service

- Description: A Scrapy-based scraper service.
- Functionality: Executes through sreality_spider.py, autonomously scraping 500 search results in the background and persisting them to the database.

## Database Service

- Description: A dedicated database service.
- Functionality: Stores data retrieved by the scraper service.

---

## Project Setup

## Setup environment variables

```bash
$ cp .env.example .env
$ vi .env
```

## Setup options

- run locally
- run with docker-compose

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
