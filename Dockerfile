FROM python:3.6

LABEL MAINTAINER="Rami sfari <rami2sfari@gmail.com>"

# Export Flask env varibles
ENV FLASK_APP manage:app

COPY ./requirements.txt ./requirements.txt

# Install Dependencies
RUN ["pip", "install", "-r", "/requirements.txt"]

# Copy files
ADD ./kanban /kanban
ADD ./db /db
WORKDIR /kanban

# Create New user & group
RUN groupadd -r uswgi && useradd -r -g uswgi uswgi
USER uswgi

EXPOSE 5000 9191

# Runtime configuration
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
