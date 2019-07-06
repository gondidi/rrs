#!/bin/bash
# sudo ln -s /var/www/html/rrs/sendmail2log.sh /usr/sbin/sendmail
echo "$0 $@" | logger -p cron.err 
logger -p cron.info
