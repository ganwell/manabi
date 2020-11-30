FROM python:3.7-slim
RUN useradd manabi
ENV PATH="/home/manabi/.local/bin:${PATH}"
WORKDIR /app
COPY --chown=manabi Pipfile \
    Pipfile.lock \
    setup.cfg \
    setup.py \
    MANIFEST.in \
    /app/
RUN mkdir c && mkdir manabi && touch manabi/__init__.py
COPY --chown=manabi c/install c/pipinstall /app/c/
RUN c/install
USER manabi
