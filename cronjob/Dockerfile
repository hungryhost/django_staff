FROM ubuntu:latest as mailer
WORKDIR /usr/src/app-staff
RUN RUNLEVEL=1 apt-get update && apt-get -y install cron

COPY crontab_mailing /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN RUNLEVEL=1 crontab /etc/cron.d/crontab
RUN RUNLEVEL=1 touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log