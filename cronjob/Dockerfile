FROM ubuntu:latest
WORKDIR /usr/src/app-staff
RUN RUNLEVEL=1 apt-get update && apt-get -y install cron
RUN echo exit 0 > /usr/sbin/policy-rc.d
# Add crontab file in the cron directory
ADD crontab_mailing /etc/cron.d/simple-cron

# Add shell script and grant execution rights
ADD mailing.sh /mailing.sh
RUN chmod +x /mailing.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log