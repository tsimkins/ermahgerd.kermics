from kermics import app
from kermics.download import ComicDownloaderFactory
import time
from datetime import datetime
import random

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

config = app.config.get('COMICS_CONFIG')

datestamp = datetime.now().strftime('%Y%m%d')

# Get comic names
comics = config.sections()

# Random order every time
random.shuffle(comics)

for s in comics:
    print "Download %s" % s
    z = ComicDownloaderFactory(s, datestamp)
    if z.download():
        sleep_time = random.randint(10,20)
        print "Sleeping %d" % sleep_time
        time.sleep(sleep_time)
