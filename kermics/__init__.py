from flask import Flask, render_template, send_file, request, make_response, redirect, url_for
from kermics.models import Comic, ComicSeries, get_comic_series, get_comic, \
                           get_daily_comics, get_all_series, get_today, get_dates
import magic
import locale
from datetime import datetime
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

app = Flask(__name__)

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

ITEMS_PER_PAGE = app.config.get('ITEMS_PER_PAGE')

def get_comic_filter(request):
    comic_filter = request.cookies.get('comic_filter')

    if not comic_filter:
        return [x.key for x in get_all_series()]
    
    return comic_filter.split('|')

def format_date(i):
    try:
        j = datetime.strptime(i, '%Y%m%d')
        return j.strftime('%A %B %d, %Y')
    except:
        return i

app.jinja_env.globals.update(get_comic_filter=get_comic_filter)
app.jinja_env.globals.update(format_date=format_date)

@app.route("/", methods=['GET'])
@app.route("/date/<published_date>", methods=['GET'])
def index(published_date=None):

    if not published_date:
        published_date = get_today()

    comics = get_daily_comics(published_date)

    return render_template('index.html', 
                            title="Comics for %s" % format_date(published_date), 
                            comics=comics
                            )

@app.route("/date", methods=['GET'])
def date():

    return render_template('dates.html', 
                            title="Comics By Date", 
                            dates=get_dates()
                            )
                            
@app.route("/strip", methods=['GET'])
def series():
    return render_template('strip.html', 
                            title="Comic Strips", 
                            series=get_all_series()
                            )

@app.route("/strip/<key>", methods=['GET'])
@app.route("/strip/<key>/<page_number>", methods=['GET'])
def comics(key=None, page_number=1):

    series = get_comic_series(key)

    if not series:
        return redirect(url_for('series'))

    comics = series.comics.order_by(Comic.published_date.desc()).paginate(int(page_number), ITEMS_PER_PAGE, False)
    
    return render_template('comics.html', key=key, title=series.title, 
                            series=series, comics=comics, 
                            page_number=page_number)

@app.route("/comic/<key>/<published_date>", methods=['GET'])
@app.route("/comic/<key>/<published_date>/<original_date>", methods=['GET'])
def comic(key=None, published_date=None, original_date=None):
    comic = get_comic(key, published_date, original_date)
    image_url = comic.image_url
    mimetype = magic.from_file(image_url, mime=True)
    return send_file(image_url, mimetype=mimetype)
    

@app.route("/config", methods=['GET'])
def config():
    comics = get_all_series()
    
    return render_template('config.html', 
                            title="Configuration", 
                            comics=comics
                            )

@app.route("/config", methods=['POST'])
def config_post():
    config_comic = request.form.getlist('config_comic')
    comic_filter = "|".join(config_comic)
    resp = make_response( redirect(url_for('index')))
    resp.set_cookie('comic_filter', comic_filter)    
    return resp