FROM debian:bookworm
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install xinetd python3 python3-pip
RUN rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED
RUN pip install pycryptodome
RUN groupadd -r crypto && useradd -r -g crypto crypto
ADD challenge/crypto.xinetd	/etc/xinetd.d/crypto
ADD challenge/init.sh	/etc/init.sh
ADD challenge/redir.sh	/home/crypto/redir.sh
RUN chmod 550	/home/crypto/redir.sh
RUN chmod 700	/etc/init.sh
RUN chmod 1733	/tmp /var/tmp /dev/shm
ADD n0psichu.py	/home/crypto/n0psichu.py
RUN chmod 550	/home/crypto/n0psichu.py
ADD secret.py	/home/crypto/secret.py
RUN chmod 440	/home/crypto/secret.py
RUN chown -R root:crypto /home/crypto
RUN ls /home/crypto -lh
RUN service xinetd restart
EXPOSE 12431
CMD ["/etc/init.sh"]