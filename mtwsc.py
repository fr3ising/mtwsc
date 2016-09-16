from datetime import datetime
from sets import Set
from bs4 import BeautifulSoup
import re
import requests
import urlparse
import Queue
from threading import Thread

class Mtwsc(object):

    def __init__(self,url,limit=10,pattern=False):
        r = requests.get(url,timeout=5)
        self.q = Queue.LifoQueue()
        data = r.text
        self.hilos = []
        soup = BeautifulSoup(data.encode('utf-8'),"lxml")
        self.urls = []
        for href in soup.findAll('a',href=True):
            if pattern:
                if pattern.search(href['href']):
                    if ( len(self.urls) < limit ):
                        self.q.put(urlparse.urljoin(url, href['href']))
                        self.urls.append(urlparse.urljoin(url, href['href']))
        return

    def grab_data(self):
        while not self.q.empty():
            url = self.q.get()
            try:
                r = requests.get(url.strip())
                self.hilos.append(r.text)
                print "Incorporado %s" % url.strip()
            except:
                print "!!! Error en hilo %s" % url.strip()
            self.q.task_done()

    def download(self,threads=1):
        for i in range(threads):
            th = Thread(target=self.grab_data)
            th.start()
        self.q.join()

    def parse_data(self):
        self.status = Set()
        for hilo in self.hilos:
            soup = BeautifulSoup(hilo.encode('utf-8'),"lxml")
            online = re.compile(r'user_online\.gif',re.U)
            for img in soup.findAll('img',src=True,alt=True):
                if online.search(img['src']):
                    self.status.add(img['alt'])
            

if __name__ == "__main__":
    url = "http://forocoches.com"
    forocoches = Mtwsc('http://forocoches.com',50,re.compile(r'showthread\.php\?t=',re.U))
    startTime = datetime.now()
    print "Scraping ..."
    forocoches.download(10)
    print datetime.now()-startTime
    forocoches.parse_data()
    for s in forocoches.status:
        print s.encode('utf-8')
