from kermics.download import ComicDownloader
from BeautifulSoup import BeautifulSoup
import re
from datetime import datetime

class KingFeaturesDownloader(ComicDownloader):

    def getRefererURL(self):
        return 'http://comicskingdom.com/comics'

    def getComicPageURL(self):
        # Get the base URL for the comic
        base_url = self.getURL()
        
        if not base_url:
            return None

        date_obj = self.getDatestampObject()

        # And YYYY-MM-DD datesatmp
        formatted_datestamp = date_obj.strftime('%Y-%m-%d')
        
        # Concatenate
        return '%s/%s' % (base_url, formatted_datestamp)

    def getComicJSURL(self):
        comic_page_url = self.getComicPageURL()
        
        br = self.getBrowser()
        
        if not comic_page_url:
            # Read Numeric id/code from Config
            comic_id = self.getConfig('id')
            
            # If the day is a sunday, try for the id_sunday (to handle Phantom)
            if self.isSunday():
                comic_id = self.getConfig('id_sunday', comic_id)

            # Comic short name
            comic_name = self.strip
    
            # Comic date
            comic_date = self.datestamp
    
            if self.isVintage():
                return "http://safr.kingfeatures.com/idn/ck3/series/js/index.php?cn=32&zn=712&sn=%s&wt=4&fs=0&fd=%s&null=0" % (comic_id, comic_date)
            else:
                return "http://safr.kingfeatures.com/idn/ck3/zone/js/index.php?cn=32&zn=62&fn=%s&wt=0&fs=0&fd=%s&null=0" % (comic_id, comic_date)
        
        comic_page_request = br.open(comic_page_url)
        
        html = comic_page_request.read()
        
        soup = BeautifulSoup(html)
        
        img = soup.find('img', attrs={'class' : 'safr'})
        
        if img:
            return 'http:%s' % img.get('data-src', None)

        return None        

    def downloadComic(self):
    
        comic_date = self.datestamp
        comic_name = self.strip
    
        js_url = self.getComicJSURL()
        br = self.getBrowser()

        # Attempt to open JavaScript URL
        try:
            script_request = br.open(js_url)
        except:
            print "Error with comic URL %s" % js_url
            return False

        js = script_request.read()

        if self.isVintage():
            date_regex = re.compile("Original\s*Publication\s*Date\s*:\s*.*?,\s*([A-Za-z]+\s*\d{1,2},\s*\d{4})")
            date_match = date_regex.search(js)
            if date_match:
                date_output = datetime.strptime(date_match.group(1), '%B %d, %Y').strftime('%Y%m%d')
            else:
                date_output = '_' + comic_date
        else:
            date_output = comic_date

        img_src_regex = re.compile("src\s*=\s*'(.*?)'")

        img_match = img_src_regex.search(js)
        img_url = img_match.group(1)

        (img_data, extension) = self.downloadImage(br, img_url)

        filename = "%s-%s.%s" % (comic_name, date_output, extension)

        # Save the comic to the filesystem
        self.writeComic(filename, img_data)

        return True # Causes sleep on successful download