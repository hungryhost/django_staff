FROM python:3.8.6 as builder

WORKDIR /usr/src/app-staff

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
COPY crontab_mailing .
COPY mailing.sh .
RUN apt-get update && apt-get -y install cron
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

# set work directory
WORKDIR /usr/src/app-staff
ADD . /usr/src/app-staff
RUN mkdir  ./logs/
RUN chmod 755 -R /usr/src/app-staff/
RUN chmod +rwx ./logs/
# setup cron


#CMD  ['python manage.py migrate --noinput']
FROM ubuntu:latest
WORKDIR /usr/src/app-staff
COPY crontab_mailing /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log