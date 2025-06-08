FROM httpd:latest

COPY ./*.html /usr/local/apache2/htdocs/
COPY ./*.js /usr/local/apache2/htdocs/
COPY ./styles.css /usr/local/apache2/htdocs/
COPY ./*.png /usr/local/apache2/htdocs/
COPY ./front.conf /usr/local/apache2/conf/httpd.conf
COPY ./git /usr/local/apache2/htdocs/.git