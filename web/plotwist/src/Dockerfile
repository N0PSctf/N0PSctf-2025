FROM debian:bullseye

# Install necessary packages
RUN apt -y update && apt -y install nginx python3-venv python3-pip

# Add nginx configuration
RUN rm /etc/nginx/sites-enabled/default
COPY src/plotwist_nginx.conf /etc/nginx/sites-enabled/plotwist

# rate limit
COPY src/nginx.conf /etc/nginx/nginx.conf


# Add api
WORKDIR /srv
COPY src/api plotwist
COPY flag.txt plotwist/secret_flag.txt
RUN rm -rf entrypoint.sh; chown -R :www-data plotwist

# Add front
COPY src/front/index.html /usr/share/nginx/html

# Install python dependencies
WORKDIR /usr/local
RUN mkdir venvs
WORKDIR venvs
RUN python3 -m venv plotwist_venv

# Install python dependencies into virtual environment
WORKDIR plotwist_venv
RUN . bin/activate
RUN pip install fastapi hypercorn jinja2

# Expose port 80
EXPOSE 80

# Create user
RUN useradd -u 1337 -g www-data -ms /bin/bash plotwist

# Start hypercorn and nginx
COPY src/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
