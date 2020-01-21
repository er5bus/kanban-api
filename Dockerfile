FROM python:3.6

LABEL MAINTAINER="Rami sfari <rami2sfari@gmail.com>"

# Export Flask env varibles
ENV FLASK_APP manage:app

# Copy and Install Dependencies
COPY ./requirements.txt /requirements.txt
RUN ["pip", "install", "-r", "/requirements.txt"]

# Create New user & group
RUN groupadd -r uswgi && useradd -r -g uswgi uswgi
USER uswgi

# Copy project files
COPY ./kanban /kanban

WORKDIR /kanban

EXPOSE 5000 9191

# Runtime configuration
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
