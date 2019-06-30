#!/bin/bash
# sudo ln -s /var/www/html/rrs/sendmail2log.sh /usr/sbin/sendmail
# sudo ln -sf /usr/bin/vim /etc/alternatives/editor
# sudo /etc/init.d/rsyslog restart
echo "$0 $@" | logger -p cron.err 
logger -p cron.info
