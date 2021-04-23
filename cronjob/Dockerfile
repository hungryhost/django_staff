FROM python:3.8.6 as builder
WORKDIR /usr/src/app-staff
COPY /usr/src/app-staff/requirements.txt .
COPY /usr/src/app-staff/crontab_mailing .
COPY /usr/src/app-staff/mailing.sh .
RUN chmod +rwx mailing.sh
RUN chmod +rwx crontab_mailing
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app-staff/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.6

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install dependencies
COPY --from=builder /usr/src/app-staff/wheels /wheels
COPY --from=builder /usr/src/app-staff/requirements.txt .
RUN pip install --no-cache /wheels/*

RUN RUNLEVEL=1 apt-get update && apt-get -y install cron
# Add crontab file in the cron directory
RUN echo exit 0 > /usr/sbin/policy-rc.d
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