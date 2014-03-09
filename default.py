import sys
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
from bs4 import BeautifulSoup
import os

HIS1 = "http://58.65.128.10:906"

ENG1AG = "http://58.65.128.10:604"
ENG1HR = "http://58.65.128.10:602"
ENG1SZ = "http://58.65.128.10:603"

TV1ENGAF = "http://58.65.128.17:604"
TV1ENGGZ = "http://58.65.128.17:605"
TV1HI = "http://58.65.128.17:606"

EVDS1 = "http://58.65.128.10:812"
HVDS1 = "http://58.65.128.10:811"

CARTS1 = "http://58.65.128.10:806"

# ------------------------------------------------------------
def fileNameFromURL(url):
    return os.path.basename(urlparse.urlsplit(url).path).replace("%20"," ").replace("?sortby=", "")

def addLink(name, url, max_elems):
    li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png")
    li.setProperty("IsPlayable", "true")
    li.setInfo( type="Video", infoLabels="" )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=li, isFolder=False, totalItems=max_elems)


def addDir(name, path, page, serverip):
    u=sys.argv[0]+"?path=%s&page=%s&serverip=%s"%(path,str(page),serverip)
    li=xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage="DefaultFolder.png")
    li.setInfo( type="Video", infoLabels={ "Title": name })
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=li,isFolder=True)


def buildMainMenu(server):
    movieshtml = urllib2.urlopen(server).read()
    soupa = BeautifulSoup(movieshtml)
    soup = soupa.table
    for link in soup.find_all('a'):
        foundurl = link.get('href')
        mainurl, extension = os.path.splitext(foundurl)
        if extension == "":
            addDir(fileNameFromURL(foundurl), mainurl.replace(' ','%20'),1, server)
        else:
            absUrl = server + foundurl
            addLink(fileNameFromURL(foundurl), absUrl.replace(' ', '%20'), 1)


# ------------------------------------------------------------

params = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)

try:
    path = params['path'][0]
except:
    path = '/'

if path == '/':
    addDir("Hindi Movies", "/HIS1/", 1, "HIS1")
    addDir("English Movies A - G", "/ENG1AG/", 1, "ENG1AG")
    addDir("English Movies H - R", "/ENG1HR/", 1, "ENG1HR")
    addDir("English Movies S - Z", "/ENG1SZ/", 1, "ENG1SZ")
    addDir("TV English A - F", "/TV1ENGAF/", 1, "TV1ENGAF")
    addDir("TV English G - Z", "/TV1ENGGZ/", 1, "TV1ENGGZ")
    addDir("TV Hindi", "/TV1HI/", 1, "TV1HI")
    addDir("English Video Songs", "/EVDS1/", 1, "EVDS1")
    addDir("Hindi Video Songs", "/HVDS1/", 1, "HVDS1")
    addDir("Cartoon Show", "/CARTS1/", 1, "CARTS1")

elif path == '/HIS1/':
    buildMainMenu(HIS1)
elif path == '/ENG1AG/':
    buildMainMenu(ENG1AG)
elif path == '/ENG1HR/':
    buildMainMenu(ENG1HR)
elif path == '/ENG1SZ/':
    buildMainMenu(ENG1SZ)
elif path == '/TV1ENGAF/':
    buildMainMenu(TV1ENGAF)
elif path == '/TV1ENGGZ/':
    buildMainMenu(TV1ENGGZ)
elif path == '/TV1HI/':
    buildMainMenu(TV1HI)
elif path == '/EVDS1/':
    buildMainMenu(EVDS1)
elif path == '/HVDS1/':
    buildMainMenu(HVDS1)
elif path == '/CARTS1/':
    buildMainMenu(CARTS1)


else:
    sip = params['serverip'][0]
    dpath = sip + path
    movieshtml = urllib2.urlopen(dpath.replace(' ', '%20')).read()
    soupa = BeautifulSoup(movieshtml)
    soup = soupa.table
    for link in soup.find_all('a'):
        foundurl = link.get('href')
        mainurl, extension = os.path.splitext(foundurl)
        if extension == "":
            addDir(fileNameFromURL(foundurl), mainurl.replace(' ','%20'),1, sip)
        else:
            absUrl = sip + foundurl
            addLink(fileNameFromURL(foundurl), absUrl.replace(' ', '%20'), 20)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
