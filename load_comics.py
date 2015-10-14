from kermics import app
from kermics.models import db, get_comic_series, get_comic, Comic, ComicSeries
import magic
import os
import re
import time

file_re = re.compile('^([a-zA-Z0-9]+)\-(\d{8})\.(gif|png)$')

valid_types = [
    'image/gif',
    'image/png',
    'image/jpeg',
    ]

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

directories = app.config.get('COMIC_FILES', {})
days = app.config.get('LOAD_COMICS_DAYS', 3)

counter = 0
increment = 100

now = time.time()
week_ago = now - days*24*60*60

for d in directories:

    for (dirpath, dirnames, filenames) in os.walk(d):

        for f in filenames:

            filename = '%s/%s' % (dirpath, f)

            # Make sure filename matches naming convention
            match_object = file_re.match(f)

            if not match_object:
                print "%s doesn't match [strip]-[date].(png|gif)" % (filename,)
                continue
            
            # Skip if file mtime is older than a week ago.
            if os.stat(filename).st_mtime < week_ago:
                print "%s too old: %d" % (filename, os.stat(filename).st_mtime)
                continue

            # Make sure mimetime is an image
            mimetype = magic.from_file(filename, mime=True)

            if mimetype not in valid_types:
                print "%s not a valid type %s" % (filename, mimetype)
                continue


            # Get comic info

            (key, original_date) = match_object.group(1,2)

            published_date = dirpath.split('/')[-1]

            vintage = (published_date != original_date)

            if vintage:
                key = '%s-vintage' % key

            comic_exists = get_comic(key, published_date, original_date)

            if comic_exists:
                print "%s already exists in database." % (filename,)
                continue
                
            series = get_comic_series(key)

            try:
                o = Comic(series.id, original_date, published_date, filename)
                db.session.add(o)
                counter = counter + 1
                if not counter % increment:
                    db.session.commit()
                print "Added %s" % filename
            except:
                print "Error %s" % filename


db.session.commit()
