#!/bin/bash

set -e

echo -e "Running $FLASK_ENV Configurations\n*****************\n"

if [ $MIGRATE_DB -eq 1 ]; then
  echo -e "Migrating the database\n************\n"
  exec flask db upgrade &
  wait $!
  echo Job exited with status $?
fi

if [ $FLASK_ENV = 'DEV' ]; then
  echo -e "Starting development server\n***********\n"
  exec flask run --host=0.0.0.0 --port 5000 --reload
elif [ $FLASK_ENV = 'TEST' ]; then
  echo -e "Running tests\n************\n"
  exec flask tests
else
  echo -e "Starting production server\n************\n"
  exec uwsgi --ini /kanban/uwsgi.ini
fi
