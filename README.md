# ermaghred.kermics

## Install

`virtualenv --no-site-packages ermahgerd.kermics` 

`cd ermahgerd.kermics`

`mkdir db data conf`

`. bin/activate`

`pip install Flask Flask-SQLAlchemy python-magic lxml BeautifulSoup mechanize`

`git clone https://github.com/tsimkins/ermahgerd.kermics.git app`

`cd app`

`python ./db_setup.py`

`python ./load_comics.py`