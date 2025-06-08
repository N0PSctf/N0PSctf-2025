FROM php:8.2-apache

RUN pecl install redis && docker-php-ext-enable redis
RUN apt-get update && apt-get install -y \
    libcurl4 \
    libcurl4-openssl-dev \
    && docker-php-ext-install curl
COPY --chown=www-data:www-data ./public_html/ /var/www/html
COPY --chown=www-data:www-data ./index.html /var/www/internal/index.html
RUN chown -R www-data:www-data /var/www/
COPY ./front.conf /etc/apache2/sites-available/front.conf
COPY ./ports.conf /etc/apache2/ports.conf
RUN a2dissite 000-default && a2ensite front && service apache2 restart

EXPOSE 80 8080