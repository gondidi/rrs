crontab.bak: crontab.cron
	crontab -l > $@
	crontab $<
	-diff -u $@ $<

OUTROOT = /var/www/html/rrs
OUTDIRS = r o t mp3

#.PHONY: install
#install: ${OUTROOT}/r/Overrides.mk /usr/sbin/sendmail
#
#${OUTROOT}/r/Overrides.mk: ${OUTROOT}/r Makefile.www r.Overrides
#	ln -s ${CURDIR}/Makefile.www ${OUTROOT}/r/Makefile
#	ln -s ${CURDIR}/r.Overrides ${OUTROOT}/r/Overrides.mk
#
#${OUTROOT}/r:;	mkdir ${OUTROOT}/r
#
#/usr/sbin/sendmail:;	sudo ln -s ${CURDIR}/sendmail2log.sh $@
