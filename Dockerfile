ARG AZLINUX_BASE_VERSION=master

# Base stage with python-build-base
FROM quay.io/cdis/python-nginx-al:${AZLINUX_BASE_VERSION} AS base

ENV appname=dictionaryutils

COPY --chown=gen3:gen3 . /${appname}

WORKDIR /${appname}

# Builder stage
FROM base AS builder

RUN dnf install -y python3-devel postgresql-devel gcc

USER gen3

COPY poetry.lock pyproject.toml /${appname}/

RUN poetry install -vv --no-interaction --without dev

COPY --chown=gen3:gen3 . /${appname}

# Run poetry again so this app itself gets installed too
# include dev because we need data-simulator to run the unit tests.
RUN poetry install -vv --no-interaction

ENV  PATH="$(poetry env info --path)/bin:$PATH"

# Final stage
FROM base

COPY --from=builder /${appname} /${appname}

# Switch to non-root user 'gen3' for the serving process
USER gen3

WORKDIR /${appname}

RUN chmod +x "/${appname}/dockerrun.bash"

CMD ["/bin/bash", "-c", "/${appname}/dockerrun.bash"]
