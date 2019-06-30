#!/bin/bash
# sudo ln -s /var/www/html/rrs/sendmail2log.sh /usr/sbin/sendmail
echo "$0 $@" | logger -p cron.err 
logger -p cron.info
# sudo /etc/init.d/rsyslog restart
# sudo ln -sf /usr/bin/vim /etc/alternatives/editor
