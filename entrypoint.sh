#!/bin/bash
cd /project
/usr/local/bin/gunicorn --config /project/deploy/gunicorn.conf --log-config /project/deploy/logging.conf app:app
