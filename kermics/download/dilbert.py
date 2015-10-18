from kermics.download import ComicDownloader
from BeautifulSoup import BeautifulSoup

class DilbertDownloader(ComicDownloader):

    def getComicPageURL(self):
        # Get the base URL for the comic
        base_url = self.getURL()
        
        if not base_url:
            return None
        
        # Concatenate
        return '%s/%s' % (base_url, self.getFormattedDatestamp)

    def downloadComic(self):
        br = self.getBrowser()

        comic_page_url = self.getComicPageURL()
        
        try:
            comic_page_request = br.open(comic_page_url)
        except:
            return False
        
        html = comic_page_request.read()
        
        soup = BeautifulSoup(html)
        
        img = soup.find('img', attrs={'class' : 'img-responsive img-comic'})
        
        if img:
            img_url = img.get('src', '')

            # Get the image data and extension            
            (img_data, extension) = self.downloadImage(br, img_url)

            filename = "%s-%s.%s" % (self.strip, self.datestamp, extension)

            # Save the comic to the filesystem
            self.writeComic(filename, img_data)
            
            return True # Causes sleep on successful download
