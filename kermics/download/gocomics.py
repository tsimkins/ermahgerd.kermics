from kermics.download import ComicDownloader
from BeautifulSoup import BeautifulSoup
from datetime import timedelta

class GoComicsDownloader(ComicDownloader):

    def getVintageDate(self):
        offset = self.getConfig('offset')
        offset_sunday = self.getConfig('offset_sunday')
        
        if self.isSunday() and offset_sunday:
            offset = offset_sunday

        date_obj = self.getDatestampObject()

        if offset:
    
            delta = timedelta(days=int(offset))
            
            offset_date_obj = date_obj - delta
    
            return offset_date_obj.strftime('%Y%m%d')  

        else:
            return date_obj.strftime('%Y%m%d')
        
    def getDatestampFormat(self):
        return '%Y/%m/%d'

    def getComicPageURL(self):
        # Get the base URL for the comic
        base_url = self.getURL()
        
        if not base_url:
            return None
        
        # Concatenate
        return '%s/%s' % (base_url, self.getFormattedDatestamp())

    def downloadComic(self):
        br = self.getBrowser()

        comic_page_url = self.getComicPageURL()
        
        try:
            comic_page_request = br.open(comic_page_url)
        except:
            return False
        
        html = comic_page_request.read()
        
        soup = BeautifulSoup(html)
        
        img = soup.find('img', attrs={'class' : 'strip'})
        
        if img:
            img_url = img.get('src', '')

            # Get the image data and extension            
            (img_data, extension) = self.downloadImage(br, img_url)

            if self.isVintage():
                vintage_date = self.getVintageDate()
                filename = "%s-%s.%s" % (self.strip, vintage_date, extension)
            else:
                filename = "%s-%s.%s" % (self.strip, self.datestamp, extension)

            # Save the comic to the filesystem
            self.writeComic(filename, img_data)

            return True # Causes sleep on successful download