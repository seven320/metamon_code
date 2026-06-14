FROM python:3.13-alpine AS base

# 実行時ツール＋本番コンテナ調査用（make exec で入って vim 等を使う）。
# --no-cache が一時索引を取得するため apk update は不要。
RUN apk --no-cache add \
    curl \
    tmux \
    git \
    make \
    vim \
    tree \
    busybox-static

WORKDIR /app

# uv はインストーラDLせず公式イメージから固定版をコピー（決定的・キャッシュ安定）
COPY --from=ghcr.io/astral-sh/uv:0.4.29 /uv /uvx /bin/
ENV UV_SYSTEM_PYTHON=1

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen
ENV PATH="/app/.venv/bin:${PATH}"

COPY ./src ./src
COPY ./tests ./tests
COPY ./images ./images
COPY ./env ./env
COPY ./crontab /var/spool/cron/crontabs/root

ENV USER mother
ENV HOME /home/${USER}
ENV SHELL /bin/sh

FROM base AS dev
CMD ["sh"]

FROM base AS prd
CMD ["busybox", "crond", "-l", "2", "-L", "/dev/stderr", "-f"]
