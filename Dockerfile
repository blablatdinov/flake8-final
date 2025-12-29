# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

FROM python:3.14.2-slim
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV EC_VERSION="v3.0.3"
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
RUN cd /app
RUN pip install poetry==2.1.3
RUN apt-get update && apt-get install curl git -y
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /bin
RUN curl -O -L -C - https://github.com/editorconfig-checker/editorconfig-checker/releases/download/$EC_VERSION/ec-linux-amd64.tar.gz && \
    tar xzf ec-linux-amd64.tar.gz -C /tmp && \
    mkdir -p /root/.local/bin && \
    mv /tmp/bin/ec-linux-amd64 /root/.local/bin/ec
COPY poetry.lock pyproject.toml /app/
COPY lint-requirements.txt /app/
RUN python3 -m venv lint-venv
RUN ./lint-venv/bin/pip install -r lint-requirements.txt
# RUN poetry install
COPY . .
