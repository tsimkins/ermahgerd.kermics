from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

app = Flask(__name__)

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

db = SQLAlchemy(app)

def get_all_series():
    return ComicSeries.query.order_by('title').all()

def get_comic_series(k, vintage=False):

    if vintage:
        k = '%s-vintage' % k
        
    return ComicSeries.query.filter(ComicSeries.key==k).first()

def get_comic(k, p, o=None):
    series = get_comic_series(k)
    if not series:
        return None
    if o:
        return Comic.query.filter(Comic.series_id==series.id, Comic.published_date==p, Comic.original_date==o).first()
    else:
        return Comic.query.filter(Comic.series_id==series.id, Comic.published_date==p, Comic.original_date==p).first()

def get_today():
    return db.session.query(db.func.max(Comic.published_date)).scalar()

def get_dates():
    dates = db.session.query(db.func.distinct(Comic.published_date)).order_by(Comic.published_date.desc()).all()
    return [x[0] for x in dates]

def get_daily_comics(date=None):

    if not date:
        date = db.session.query(db.func.max(Comic.published_date)).scalar()
        
    return Comic.query.filter(Comic.published_date==date).join(ComicSeries).order_by('comic_series.title').all()

class ComicSeries(db.Model):

    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128))
    title = db.Column(db.String(512))
    
    comics = db.relationship('Comic', backref='series', lazy='dynamic')
    
    def __init__(self, key, title):
		self.key = key 
		self.title = title 

    def __repr__(self):
        return '<ComicSeries "%s: %s">' % (self.key, self.title)

class Comic(db.Model):

    __table_args__ = {'sqlite_autoincrement': True}
    
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.String(128), db.ForeignKey('comic_series.id'))
    original_date = db.Column(db.String(128), nullable=True)
    published_date = db.Column(db.String(128), nullable=True)
    image_url = db.Column(db.String(1024))
    
    def __init__(self, series_id, original_date, published_date, image_url):
		self.series_id = series_id 
		self.original_date = original_date 
		self.published_date = published_date 
		self.image_url = image_url 

    def __repr__(self):
        return '<Comic "%s">' % (self.image_url.split('/')[-1])