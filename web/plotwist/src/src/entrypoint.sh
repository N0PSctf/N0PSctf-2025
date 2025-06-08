#!/bin/bash

# Start hypercorn as the plotwist user in the background
cd /srv/plotwist
source /usr/local/venvs/plotwist_venv/bin/activate
su -s /bin/bash -c "hypercorn main:app" plotwist &

# Start nginx in the foreground as root
nginx -g "daemon off;"
