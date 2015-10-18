import re
import os
from datetime import datetime
from kermics import app, datestamp_to_date
import mechanize
import cookielib

app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

MIN_SIZE = app.config.get('MIN_SIZE', 1024)

fme = app.config.get('FILE_MIMETYPE_EXTENSION', {})

file_re = re.compile('^(.*?)\-\d{8}\.([a-z]{3})')

class ComicDownloader:

    def __init__(self, strip, datestamp=None):
        self.strip = strip

        if datestamp:
            self.datestamp = datestamp
        else:
            self.datestamp = self.getCurrentDateStamp()

        self.config = self.readConfig()

    def currentDate(self):
        return datetime.now()

    def getCurrentDateStamp(self):
        return self.currentDate().strftime('%Y%m%d')

    def getDatestampObject(self):
        return datestamp_to_date(self.datestamp)

    def getDatestampFormat(Self):
        return '%Y-%m-%d'

    def getFormattedDatestamp(self):
        date_obj = self.getDatestampObject()
        return date_obj.strftime(self.getDatestampFormat())  

    def isSunday(self):
        date_obj = self.getDatestampObject()
        return (date_obj.weekday() == 6)

    def readConfig(self):
        return app.config.get('COMICS_CONFIG', None)

    def getConfig(self, v, default=None):
        try:
            return self.config.get(self.strip, v)
        except:
            return default

    def isVintage(self):
        return ('vintage' in self.strip)

    def getProvider(self):
        return self.getConfig('provider')

    def getOutputDirectory(self):
        output_root = app.config.get('COMIC_OUTPUT')
        datestamp = self.getDatestampObject().strftime('%Y%m%d')
        output_directory = '%s/%s' % (output_root, datestamp)

        if not os.path.exists(output_directory):
            os.mkdir(output_directory, 0755)

        return output_directory

    def comicExists(self):
        output_directory = self.getOutputDirectory()

        for f in os.listdir(output_directory):
            match_object = file_re.match(f)
            if match_object and match_object.group(1) == self.strip:
                filename = '%s/%s' % (output_directory, f)
                if os.stat(filename).st_size > MIN_SIZE:
                    return True

        return False

    def getRefererURL(self):
        return self.getURL()

    def getBrowser(self, referer_url=None):
    
        if not referer_url:
            referer_url = self.getRefererURL()
    
        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(False)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Set browser headers
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.7; en-US; rv:1.9.2.22) Gecko/20110902 Firefox/3.6.22'), ('Referer', referer_url)]

        return br

    def getURL(self):
        return self.getConfig('url', None)

    def download(self):
        # Don't try to download if the comic exists
        if self.comicExists():
            return False

        # if the current day is not Sunday, and it's a Sunday comic
        if self.getConfig('sunday', False) and not self.isSunday():
            return False

        return self.downloadComic()

    def downloadComic(self):
        pass

    def downloadImage(self, br, img_url):
        img_response = br.open(img_url)
        img = img_response.read()

        content_type = img_response.info().getheader('Content-Type')

        extension = fme.get(content_type, 'data')
        
        return (img, extension)

    def writeComic(self, filename, img_data):
        output_directory = self.getOutputDirectory()
        
        output_file = "%s/%s" % (output_directory, filename)

        f=open(output_file, 'w')
        f.write(img_data)
        f.close()
        
        # Make a hard link to the non-vintage filename for backwards compatibility
        if self.isVintage():
            vintage_file = output_file.replace('-vintage', '')
            
            if not os.path.exists(vintage_file):
                os.link(output_file, vintage_file)

# To avoid circular import, import the sub-downloaders after the main class is
# created.

import kingfeatures, gocomics, dilbert

def ComicDownloaderFactory(strip, datestamp=None):

    z = ComicDownloader(strip, datestamp)

    provider = z.getProvider()

    if provider == 'kingfeatures':
        return kingfeatures.KingFeaturesDownloader(strip, datestamp)
    elif provider == 'gocomics':
        return gocomics.GoComicsDownloader(strip, datestamp)
    elif provider == 'dilbert':
        return dilbert.DilbertDownloader(strip, datestamp)
    else:
        return z