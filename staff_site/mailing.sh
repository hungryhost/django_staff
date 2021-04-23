echo "$(date): executed script" >> /var/log/cron.log 2>&1
python /usr/src/app-staff/manage.py submit_newsletter 1>/dev/null 2>&1