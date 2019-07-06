#! /usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, pathlib, datetime, time, requests, json, subprocess
from email import utils
args = sys.argv
usage = "Usage : rec.py channel(FM|R1|R2) duration(minuites) [progname (channel)] [cutoff] [filenamepattern ('+%m%d%%%H%M%S')] | rec.py -mode norec"
documentroot = pathlib.Path('/var/www/html')
mode = all
if len(args) < 3:
  print(usage)
  sys.exit()
channel = args[1]
if channel == 'R1':
  ch= "r1"
  m3u8url="https://nhkradioakr1-i.akamaihd.net/hls/live/511633/1-r1/1-r1-01.m3u8"
elif channel == 'R2':
  ch= "r2"
  m3u8url="https://nhkradioakr2-i.akamaihd.net/hls/live/511929/1-r2/1-r2-01.m3u8"
elif channel == 'FM':
  ch= "r3"
  m3u8url="https://nhkradioakfm-i.akamaihd.net/hls/live/512290/1-fm/1-fm-01.m3u8"
elif channel == '-mode':
  if args[2] == 'norec':
    mode = 'norec'
  else:
    print(args[0], ": Invalid mode", args[2])
    print(usage)
    sys.exit()
else:
  print(args[0], ": Invalid channel", channel)
  print(usage)
  sys.exit()
#print("ch=", ch)
if mode != 'norec':
  duration = int(args[2]) * 60 + 10
  #print("duration=", duration)
  if len(args) > 3:
    progname = args[3]
  else:
    progname = channel
  #print("progname=", progname)
  filename = ""
  epidsc = ""
  try:
    present = requests.get("http://api.nhk.or.jp/v2/pg/now/130/" + ch +".json?key=Ym2qyF2CRLGVlRQbnaAtRxqAbGEXTMxS").json()["nowonair_list"][ch]["present"]
    filename = present["title"]
    epidsc = present["subtitle"]
  except:
    pass
  if len(filename) < 2:
    filename = progname
  if len(epidsc) > 0:
    epidsc = filename + "▽" + epidsc
  else:
    epidsc = filename
  filename = "".join(epidsc.split())
  if len(args) > 4: #cutoff
    cutoff = args[4]
    if len(cutoff) > 0:
  #    print("cutoff=", cutoff)
      filename = filename[filename.find(cutoff)+1:]
  filename = filename[0:20]
  #print("filenane=", filename)
  #print("epidesc=", epidsc)
  if len(args) > 5: # datepattern
    filenamepattern = datetime.datetime.today().strftime(args[5])
  else:
    filenamepattern = datetime.datetime.today().strftime("%m%d{}%H%M")
  #print("filenamepattern=", filenamepattern)
  filename = filenamepattern.format(filename)
  #print("filenane=", filename)
  ffmpeg = ["/usr/bin/ffmpeg", "-loglevel", "quiet", "-y", "-i", m3u8url, "-to", str(duration), "-metadata", "genre=Radio", "-metadata", "artist=" + channel, "-metadata", "album=" + progname, "-c", "copy", filename + ".m4a"]
  #print("ffmpeg=", ffmpeg)
  subprocess.check_call(ffmpeg)
  with open(filename + ".dsc", 'w') as f:
    f.write(epidsc)
# endif norec  
podparams = {
  "podtitle": "MyRadio",
  "maxfiles": 50,
  "minfiles":  1,
  "maxdays":  50,
  "maxdu":  1000
  }
#print("j=", type(j), json.dumps(j))
try:
  ini = json.load(open('ini.json', 'r'))
except FileNotFoundError:
  ini = {}
diff = ini.keys() - podparams.keys()
#print("diff=", diff)
if len(diff) > 0:
  print("Invalid ini.json key:", diff)
  sys.exit()
podparams.update(ini)
#print("j=", type(j), json.dumps(j))
p = pathlib.Path(".")
exts = ["*.m4a", "*.mp3", "*.aac"]
files = [f for fs in [list(p.glob(ext)) for ext in exts] for f in fs]
maxfiles = podparams["maxfiles"]
minfiles = podparams["minfiles"]
if len(files) > minfiles and  maxfiles > 0 and len(files) > maxfiles:
  files.sort(key=lambda x: x.stat().st_mtime)
  for f in files[:len(files) - maxfiles]:
    #print("removing: ", f)
    os.remove(f)
maxdays = podparams["maxdays"]
maxdays = datetime.datetime.now().timestamp() - maxdays * 60 * 60 * 24
#files = list(p.glob("*.m4a"))+list(p.glob("*.mp3"))+list(p.glob("*.aac"))
files = [f for fs in [list(p.glob(ext)) for ext in exts] for f in fs]
if len(files) > minfiles:
  files.sort(key=lambda x: x.stat().st_mtime)
  for f in files[:-minfiles]:
    if os.stat(f).st_mtime < maxdays:
      #print("removing: ", f)
      os.remove(f)
    else:
      break
maxdu = podparams["maxdu"]
#files = list(p.glob("*.m4a"))+list(p.glob("*.mp3"))+list(p.glob("*.aac"))
files = [f for fs in [list(p.glob(ext)) for ext in exts] for f in fs]
if len(files) > minfiles:
  files.sort(key=lambda x: x.stat().st_mtime)
  for f in files[:-minfiles]:
    du = int(subprocess.check_output("du -sm".split()).decode().split()[0])
    if du > maxdu:
      #print("removing: ", f)
      os.remove(f)
    else:
      break
#files = list(p.glob("*.m4a"))+list(p.glob("*.mp3"))+list(p.glob("*.aac"))
files = [f for fs in [list(p.glob(ext)) for ext in exts] for f in fs]
files = [os.path.splitext(f)[0] for f in files]
for f in list(p.glob("*.dsc")):
  if os.path.splitext(f)[0] in files:
    pass
  else:
    #print("removing: ", f)
    os.remove(f)
podtitle = podparams["podtitle"]
poddsc = "".join((str(du) + "M" + subprocess.check_output('df .'.split()).decode().split()[-2] + open("/sys/class/thermal/thermal_zone0/temp","r").read()[0:3] + "'C" + subprocess.check_output(['uptime']).decode()).split())
hosts = [[os.uname()[1], '0']]
hosts += [[l.split()[1].split('/')[0], l.split()[7]] for l in subprocess.check_output('ip a'.split()).decode().splitlines() if "global" in l]
#print(hosts)
for host in hosts:
  publicurl = "http://" + host[0] + "/" + str(documentroot.cwd().relative_to(documentroot))
  with open(host[1] + ".xml", "w") as xml:
    xml.write('''\
<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
  <channel>
    <title>{podtitle}</title>
    <itunes:author>{poddsc}</itunes:author>
    <itunes:image href="{publicurl}/image.jpg" />\
  '''.format(podtitle = podtitle, poddsc = poddsc, publicurl = publicurl))
    files=list(p.glob("*.m4a"))+list(p.glob("*.mp3"))+list(p.glob("*.aac"))
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    for f in files:
      name = f.stem
      try:
        epidsc = open(f.with_suffix('.dsc'), 'r').read()
      except FileNotFoundError:
        epidsc = ""
      url = publicurl + "/" + f.name
      length = f.stat().st_size
      if f.suffix == ".mp3":
        mime = 'audio/mp3'
      else:
        mime = 'audio/mp4'
      date=utils.formatdate(f.stat().st_mtime, localtime=True)
      xml.write('''
    <item>
      <title>{name}</title>
      <description>{epidsc}</description>
      <enclosure url="{url}"
                 length="{length}"
                 type="{mime}" />
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{date}</pubDate>
    </item>\
  '''.format(name=name, epidsc=epidsc, url=url, length=length, mime=mime, date=date))
    xml.write('''
  </channel>
</rss>''')
