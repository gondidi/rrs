crontab.bak: crontab
	crontab -l > $@
	crontab $<
	-diff -u $@ $<
