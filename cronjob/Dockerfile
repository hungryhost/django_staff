FROM ubuntu:latest as mailer
WORKDIR /usr/src/app-staff
RUN echo exit 0 > /usr/sbin/policy-rc.d
RUN RUNLEVEL=1 apt-get update && apt-get -y install cron
RUN chmod 0644 /etc/cron.d/crontab
COPY crontab_mailing /etc/cron.d/crontab
COPY mailing.sh .
RUN chmod +rwx mailing.sh
RUN chmod +rwx crontab_mailing
RUN RUNLEVEL=1 crontab /etc/cron.d/crontab
RUN RUNLEVEL=1 touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log