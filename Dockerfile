FROM nginx:1.9
MAINTAINER David Bourasseau <david.bourasseau@gmail.com>

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN apt-get install python-pip mediainfo python-dev libxslt1-dev python-dev  zlib1g-dev -y
RUN pip install watchdog lxml

RUN mkdir -p /vTU/vTU/input/
RUN mkdir -p /vTU/vTU/spool/
RUN mkdir -p /home/herbaut/.ssh/
RUN mkdir -p /usr/share/nginx/html/output
RUN useradd herbaut
RUN ln -s /usr/share/nginx/html/output/ /vTU/vTU/

RUN chown -R herbaut /vTU/
RUN chown -R herbaut /home/herbaut/

COPY sshkeydocker.pub sshkeydocker.pub
RUN cat sshkeydocker.pub >> /home/herbaut/.ssh/authorized_keys

COPY adaptation/ /worker/adaptation
WORKDIR worker
RUN pwd && ls

EXPOSE 22

CMD /usr/sbin/sshd  && nginx && python adaptation/commons.py
