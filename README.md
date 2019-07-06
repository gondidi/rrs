# usage
`Usage : rec.py channel(FM|R1|R2) duration(minuites) [progname (channel)] [cutoff] [filenamepattern ('+%m%d%%%H%M%S')] | rec.py -mode norec`

# configuration
`documentroot = pathlib.Path('/var/www/html')`

# installation

# variable definitions
* podcast
  * poddir -> current directory
  * ini.json
    * podtitle
    * maxdays
    * maxfiles
    * minfiles
    * maxdu
  * image.jpg
  * poddsc
* program
  * start_time (through cron)
  * channel
  * duration
  * progname
  * cutoff
  * filenameformat
* episode
  * filename.m4a
  * epidsc.dsc description
