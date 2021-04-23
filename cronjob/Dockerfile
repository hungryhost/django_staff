FROM python:3.8.6 as builder
RUN printf '#!/bin/sh\nexit 0' > /usr/sbin/policy-rc.d
WORKDIR /usr/src/app-staff
COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app-staff/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image

FROM python:3.8.6
WORKDIR /usr/src/app-staff

RUN printf '#!/bin/sh\nexit 0' > /usr/sbin/policy-rc.d
# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install dependencies
COPY --from=builder /usr/src/app-staff/wheels /wheels
COPY --from=builder /usr/src/app-staff/requirements.txt .
RUN pip install --no-cache /wheels/*
