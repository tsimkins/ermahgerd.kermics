
from kermics import app
from kermics.models import db, get_comic_series, get_comic, Comic, ComicSeries
import magic
import os
import re

file_re = re.compile('^([a-zA-Z0-9]+)\-(\d{8})\.(gif|png)$')

valid_types = [
    'image/gif',
    'image/png',
    'image/jpeg',
    ]

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

directories = app.config.get('COMIC_FILES', {})

counter = 0
increment = 100

for d in directories:
    for (dirpath, dirnames, filenames) in os.walk(d):
        for f in filenames:
            filename = '%s/%s' % (dirpath, f)
            mimetype = magic.from_file(filename, mime=True)
            if mimetype in valid_types:
                match_object = file_re.match(f)
                if match_object:
                    (key, original_date) = match_object.group(1,2)
                    published_date = dirpath.split('/')[-1]
                    vintage = (published_date != original_date)
                    if vintage:
                        key = '%s-vintage' % key
                    comic_exists = get_comic(key, published_date, original_date)
                    if not comic_exists:
                        series = get_comic_series(key)
                        try:
                            o = Comic(series.id, original_date, published_date, filename)
                            db.session.add(o)
                            counter = counter + 1
                            if not counter % increment:
                                db.session.commit()
                            print "Added %s" % o
                        except:
                            import pdb; pdb.set_trace()

db.session.commit()
