FROM mcr.microsoft.com/vscode/devcontainers/python:3.10-buster
USER vscode
RUN curl -sSL https://install.python-poetry.org | python -
RUN /home/vscode/.local/bin/poetry config virtualenvs.in-project true
USER root