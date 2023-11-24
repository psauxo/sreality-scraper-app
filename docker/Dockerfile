FROM python:3.10-slim-buster as python-base
LABEL description="Dockerfile for Simple HTTP Server"

# Setup environment variables
ENV LANG="C.UTF-8"\
    LC_ALL="C.UTF-8" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION="1.4.2" \
    POETRY_HOME="/root/.local/bin" \
    PYSETUP_PATH=/usr/app/src \
    VENV_PATH="/usr/app/src/.venv/bin"

ENV PATH="/root/.local/bin/bin:$PATH"

FROM python-base as poetry-base

WORKDIR $PYSETUP_PATH

COPY pyproject.toml poetry.lock ./
COPY . .

# Install poetry, configure it to create venvs inside the project directory and install dependencies and build wheel
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        firefox-esr \
        wget \
        libpq-dev \
    # install poetry - uses $POETRY_VERSION internally
    && curl -sSL https://install.python-poetry.org | python - \
    && export PATH="$POETRY_PATH:$PATH" \
    && poetry --version \
    && which poetry \
    \
    # configure poetry & make a virtualenv ahead of time since we only need one
    && python -m venv $VENV_PATH \
    # temporarily remove --no-dev
    && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi && poetry build -n \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

FROM poetry-base as final

# Set the non-root user as the active user
RUN groupadd --gid 1001 deploy \
    && useradd --uid 1001 --gid deploy --shell /bin/bash --create-home deploy \
    && chown -R deploy:deploy $PYSETUP_PATH \
    && chmod -R 700 $PYSETUP_PATH

# Switch to the non-root user
USER deploy

# Copy compiled wheel from python-base image
COPY --from=poetry-base --chown=deploy /usr/app/src/dist /usr/app/src/dist
COPY --from=poetry-base --chown=deploy /usr/app/src/docker /usr/app/src/docker

# Install the wheel and remove the wheel file afterwards
RUN pip install /usr/app/src/dist/*.whl && rm -rf /usr/app/src/dist && ls -la /usr/app/src/

ENTRYPOINT ["/bin/sh", "./docker/entrypoint.sh"]
