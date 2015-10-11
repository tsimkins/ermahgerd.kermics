# ermaghred.kermics

## Install

`virtualenv --no-site-packages ermahgerd.kermics` 

`cd ermahgerd.kermics`

`mkdir db data`

`. bin/activate`

`pip install Flask Flask-SQLAlchemy python-magic`

`git clone https://github.com/tsimkins/ermahgerd.kermics.git app`

`cd app`

`python ./db_setup.py`

`python ./load_comics.py`