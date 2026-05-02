#!/bin/bash

# Start SSH daemon
service ssh start

# Start the Flask app with Gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 2 app:app
