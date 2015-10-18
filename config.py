from ConfigParser import SafeConfigParser

APP_ROOT = '/home/simkintr/python/projects/ermahgerd.kermics'

COMIC_OUTPUT = "%s/data" % APP_ROOT
COMIC_FILES = [COMIC_OUTPUT, ]

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/db/kermics.db' % APP_ROOT

ITEMS_PER_PAGE = 7

LOAD_COMICS_DAYS = 3

MIN_SIZE = 1024

FILE_MIMETYPE_EXTENSION = {
    'image/gif' : 'gif',
    'image/png' : 'png',
    'image/jpeg' : 'jpg',
}

# Read manually maintained config file

from ConfigParser import SafeConfigParser

COMICS_CONFIG_FILE = '%s/conf/comics.conf' % APP_ROOT
COMICS_CONFIG = SafeConfigParser()
COMICS_CONFIG.read(COMICS_CONFIG_FILE)
