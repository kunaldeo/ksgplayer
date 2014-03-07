import sys
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
import CommonFunctions
from bs4 import BeautifulSoup
import os

common = CommonFunctions
common.plugin = "SG Player"

M_SERVER1_URL = "http://58.65.128.10:906"

# ------------------------------------------------------------

def addLink(name, url, max_elems):
    li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png")
    li.setProperty("IsPlayable", "true")
    li.setInfo( type="Video", infoLabels="" )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=li, isFolder=False, totalItems=max_elems)

def addDir(name,path,page):
    u=sys.argv[0]+"?path=%s&page=%s"%(path,str(page))
    li=xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage="DefaultFolder.png")
    li.setInfo( type="Video", infoLabels={ "Title": name })
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=li,isFolder=True)

# ------------------------------------------------------------

params = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)

try:
    path = params['path'][0]
except:
    path = '/'

if path == '/':
    addDir("Movie Server", "/movies/", 1)
    addDir("TV Server", "/tvshows/", 1)

elif path == '/movies/':
    movieshtml = urllib2.urlopen(M_SERVER1_URL).read()
    soupa = BeautifulSoup(movieshtml)
    soup = soupa.table
    for link in soup.find_all('a'):
        foundurl = link.get('href')
        mainurl, extension = os.path.splitext(foundurl)
        if extension == "":
            addDir(mainurl.replace('/','').replace('?sortby=',''), mainurl.replace(' ','%20'),1)
        else:
            absUrl = M_SERVER1_URL + foundurl
            addLink(mainurl.replace('/','').replace('?sortby=',''), absUrl.replace(' ', '%20'), 1)

else:
    print "Log: Path is: " + path
    dpath = M_SERVER1_URL + path
    movieshtml = urllib2.urlopen(dpath.replace(' ', '%20')).read()
    soupa = BeautifulSoup(movieshtml)
    soup = soupa.table
    for link in soup.find_all('a'):
        foundurl = link.get('href')
        mainurl, extension = os.path.splitext(foundurl)
        if extension == "":
            addDir(mainurl.replace('/','').replace('?sortby=',''), mainurl.replace(' ','%20'),1)
        else:
            absUrl = M_SERVER1_URL + foundurl
            addLink(mainurl.replace('/','').replace('?sortby=',''), absUrl.replace(' ', '%20'), 20)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
