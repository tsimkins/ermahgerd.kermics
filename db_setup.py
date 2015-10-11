
from kermics import app
from kermics.models import db
from kermics.models import Comic, ComicSeries

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

series = app.config.get('COMIC_SERIES', {})

# Create Tables
db.create_all()

# Add Comic Serieses
for (k,v) in series.iteritems():
    if ComicSeries.query.filter(ComicSeries.key==k).count() < 1:
        o = ComicSeries(k, v)
        db.session.add(o)
        print "Added %s" % k

db.session.commit()

