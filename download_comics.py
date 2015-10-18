from kermics import app
from kermics.download import ComicDownloaderFactory
import time
from datetime import datetime
import random
import optparse

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

config = app.config.get('COMICS_CONFIG')


# grab arguments

parser = optparse.OptionParser(description='Download comics')

parser.add_option('-c', metavar='comic_name',
                   help='Short name for comic')

parser.add_option('-d', metavar='comic_date',
                   help='Comic date (YYYYMMDD). Defaults to current date.',
                   default=datetime.now().strftime('%Y%m%d'))

(options, args) = parser.parse_args()
                   
datestamp = options.d
comic_name = options.c

# Get comic names
if comic_name:
    comics = [comic_name, ]
else:
    comics = config.sections()

# Random order every time
random.shuffle(comics)

for s in comics:
    print "Download %s" % s
    z = ComicDownloaderFactory(s, datestamp)
    if z.download():
        if not comic_name:
            sleep_time = random.randint(10,20)
            print "Sleeping %d" % sleep_time
            time.sleep(sleep_time)
