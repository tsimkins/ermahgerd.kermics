
from kermics import app
from kermics.models import db
from kermics.models import Comic, ComicSeries

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

config = app.config.get('COMICS_CONFIG', {})

# Create Tables
db.create_all()

# Add Comic Serieses
for k in sorted(config.sections()):
    # Get title
    v = config.get(k, 'title')
    if ComicSeries.query.filter(ComicSeries.key==k).count() < 1:
        o = ComicSeries(k, v)
        db.session.add(o)
        print "Added %s %s" % (k,v)

db.session.commit()

