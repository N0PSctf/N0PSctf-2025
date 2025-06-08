FROM sagemath/sagemath:10.6

WORKDIR /app

COPY flag.py flag.py
COPY meago.sage meago.sage 

#####
USER root

RUN apt update
RUN apt install -y python3 
RUN apt install -y pip 
RUN apt install -y socat

#####
USER sage

RUN sage -pip install pycryptodome

EXPOSE 13337

USER sage
RUN sudo su sage

CMD ["socat", "TCP4-LISTEN:13337,reuseaddr,fork", "EXEC:'sage meago.sage',pty,stderr,echo=0,raw,iexten=0"]


