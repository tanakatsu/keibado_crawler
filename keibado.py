# encoding: utf-8
from bs4 import BeautifulSoup
import os
import urllib2
import chardet
import traceback


class Keibado:

    def fetchPage(self, url):
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        body = res.read()
        guess_enc = chardet.detect(body)
        try:
            unicode_html = body.decode(guess_enc['encoding'])
        except UnicodeDecodeError:
            print url, guess_enc
            print traceback.format_exc()
            unicode_html = None

        if not unicode_html:
            try:
                unicode_html = body.decode('shift_jisx0213')
                print 'Decoding in shift_jisx0213 is successful.'
            except UnicodeDecodeError:
                print traceback.format_exc()
                unicode_html = body

        return unicode_html

    # URL example: http://www.keibado.ne.jp/keibabook/170109/index.html
    def getHorseUrlList(self, url):
        html = self.fetchPage(url)
        if not html:
            return []

        names_urls = []
        url_prefix = os.path.dirname(url)

        soup = BeautifulSoup(html, "html.parser")

        if soup.select('table.mini'):
            list_table = soup.select('table.mini')[0]
        elif soup.select('table[bgcolor="#003300"]'):
            list_table = soup.select('table[bgcolor="#003300"]')[0]
        horses = list_table.select('a')
        for elm in horses:
            [b.extract() for b in elm.select('br')]  # remove <br>
            names_urls.append({'name': elm.string.strip(), 'url': url_prefix + '/' + elm['href']})
        return names_urls

    # URL example: http://www.keibado.ne.jp/keibabook/bn/2017.html
    def getIssueNumberList(self, url):
        html = self.fetchPage(url)
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")

        url_prefix = os.path.dirname(url)

        elms = soup.select('a')
        urls = []
        for elm in elms:
            if elm['href'].find("../") == 0:
                url = (os.path.dirname(url_prefix) + '/' + elm['href']).replace('../', '')
                urls.append(url)

        return urls

    # URL example: http://www.keibado.ne.jp/keibabook/170109/photo01.html
    def getPadockPhotoUrl(self, url):
        html = self.fetchPage(url)
        if not html:
            return None
        soup = BeautifulSoup(html, "html.parser")

        # horse name
        name_tables = soup.select('table[bgcolor="#003300"]')
        name_table = name_tables[-1]
        if name_table.select('img'):
            horse_name = name_table.select('img')[0].string
        else:
            horse_name = name_table.select('td font b')[0].string

        # image url
        if soup.select('table[width="309"]'):
            photo_table = soup.select('table[width="309"]')[0]
            if photo_table.select('img'):
                horse_image = photo_table.select('img')[0]
            else:
                horse_image = soup.select('img[width="304"]')[0]
        else:
            horse_image = soup.select('img[width="304"]')[0]
        horse_photo_url = horse_image['src']

        url_prefix = os.path.dirname(url)
        horse_photo_url = url_prefix + '/' + horse_photo_url
        return horse_photo_url, horse_name
