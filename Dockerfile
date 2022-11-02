FROM python:3.8-slim

RUN mkdir /code
WORKDIR /code

ENV VIRTUAL_ENV=/code/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install --upgrade pip poetry

COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,mode=0755,target=/root/.cache/pypoetry \
    poetry install --only main

COPY . .

CMD ["python", "-m", "src.scripts.idun", "output"]
