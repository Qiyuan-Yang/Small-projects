import requests
from bs4 import BeautifulSoup
import bs4
import re
 
def Gethtmltext(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''

def Getalbumhtml(url,startalbum = '"Activity" Case：01 -Graveyard Memory-'):
    html = Gethtmltext(url+startalbum)
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('div'):
        if tag.get('class') == ['mw-category-generated']:
            return(tag)

def Generatealbumlist(albumlist,startalbum = '"Activity" Case：01 -Graveyard Memory-'):
    for title in Getalbumhtml(url,startalbum).find_all('a'):
        if title.string == '上一页' or title.string == '下一页':
            continue
        else:
            #with open(filename,'a') as f:
                #f.write(title.string)
            albumlist.append(title.string)

def Nextpage(albumlist,startalbum = '"Activity" Case：01 -Graveyard Memory-'):
    Generatealbumlist(albumlist,startalbum = '"Activity" Case：01 -Graveyard Memory-')
    while len(albumlist) > 1:
        for i in range(len(albumlist)):
            if i != 0 or startalbum == '"Activity" Case：01 -Graveyard Memory-':
                print(albumlist[i])
        startalbum = albumlist[-1]
        albumlist = []
        Generatealbumlist(albumlist,startalbum)


url = 'https://thwiki.cc/index.php?title=%E5%88%86%E7%B1%BB:%E5%90%8C%E4%BA%BA%E4%B8%93%E8%BE%91&pagefrom='
albumlist = []
filename = 'C://localdata.txt'
#Nextpage(albumlist)
for title in Getalbumhtml(url,'"Activity" Case：01 -Graveyard Memory-').find_all('a'):
    if title.string == '上一页' or title.string == '下一页':
        continue
    else:
        albumlist.append(title.string)
#print(albumlist)
albumurl = 'https://thwiki.cc/'
#for albumname in albumlist:
    #print(Gethtmltext(albumurl+albumname))
albumname = '"Activity" Case：01 -Graveyard Memory-'
html = Gethtmltext(albumurl+albumname)
soup = BeautifulSoup(html, 'html.parser')
for tag in soup.find_all('table'):
    if tag.get('class') == ['wikitable', 'musicTable']:
        for item in tag.find_all('tr'):
            print(item.b)
            print(item.a)
            print('\n')