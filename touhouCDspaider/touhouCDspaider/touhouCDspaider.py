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

def Exportalbuminfo(albumlist,startalbum = '"Activity" Case：01 -Graveyard Memory-'):
    Generatealbumlist(albumlist,startalbum = '"Activity" Case：01 -Graveyard Memory-')
    while len(albumlist) > 1:
        for i in range(len(albumlist)):
            if i != 0 or startalbum == '"Activity" Case：01 -Graveyard Memory-':
                Getalbuminfo(albumlist[i])
        startalbum = albumlist[-1]
        albumlist = []
        Generatealbumlist(albumlist,startalbum)

def Getalbuminfo(albumname):
    albumurl = 'https://thwiki.cc/'
    html = Gethtmltext(albumurl+albumname)
    soup = BeautifulSoup(html, 'html.parser')
    text = []
    musicinfo = []
    musicinfo.append(albumname)
    for tag in soup.find_all('table'):
        if tag.get('class') == ['wikitable', 'musicTable']:
            for item in tag.find_all('tr'):
                global count
                count = 0
                try:
                    a = item.b.string
                    if a in '0102030405060708091121314151617181922324252627282933435363738394454647484955657585966768697787988990':
                        if item.a.string == None:
                            for j in item.find_all('td'):
                                pattern = '>(.*?)<span'
                                musicname = re.search(pattern,str(j))
                                if musicname:
                                    musicname = musicname.group(0)[1:-5]
                                    if '\u3000' in musicname:
                                        musicname = musicname.replace('\u3000',' ')
                                    musicinfo.append(musicname)
                        else:
                            if '\u3000' in item.a.string:
                                item.a.string = item.a.string.replace('\u3000',' ')
                            musicinfo.append(item.a.string)
                except AttributeError:
                    for td in item.find_all('td'):
                        if td.string == '原曲':
                            for ogmusic in item.find_all('a'):
                                if ogmusic.string != None:
                                    if '\u3000' in ogmusic.string:
                                        ogmusic.string = ogmusic.string.replace('\u3000',' ')
                                        musicinfo.append(ogmusic.string)
                                    else:
                                        musicinfo.append(ogmusic.string)
                    if musicinfo[-1] != albumname and musicinfo[-2] != albumname:
                        print(musicinfo)
                        count += 1
                        musicinfo = []
                        musicinfo.append(albumname)

url = 'https://thwiki.cc/index.php?title=%E5%88%86%E7%B1%BB:%E5%90%8C%E4%BA%BA%E4%B8%93%E8%BE%91&pagefrom='
albumlist = []
filename = 'C://localdata.txt'
Exportalbuminfo(albumlist)
print(count)
'''
for title in Getalbumhtml(url,'"Activity" Case：01 -Graveyard Memory-').find_all('a'):
    if title.string == '上一页' or title.string == '下一页':
        continue
    else:
        albumlist.append(title.string)
'''
#print(albumlist)
#for albumname in albumlist:
    #print(Gethtmltext(albumurl+albumname))
#albumname = '"Activity" Case：01 -Graveyard Memory-'
#albumname = '東方幻奏響REVIVAL'

    

'''
version2：
i = 0
while i != len(text):
    try:
        item = text[i]
        if item.a.string == None:
            for j in item.find_all('td'):
                pattern = '>(.*?)<span'
                musicname = re.search(pattern,str(j))
                if musicname:
                    print(musicname.group(0)[1:-5])
            i += 3
            for ogmusic in text[i].find_all('a'):
                if ogmusic.string != None:
                    print(ogmusic.string)
            i += 1
        else:
            print(item.a.string)
            i += 5
            for ogmusic in text[i].find_all('a'):
                if ogmusic.string != None:
                    print(ogmusic.string)
            i += 1
    except:
        continue
version1：
            try:
                num = item.b.string
                if num in '0102030405060708091011213141516171819':
                    if item.a.string == None:
                        for i in item.find_all('td'):
                            pattern = '>(.*?)<span'
                            musicname = re.search(pattern,str(i))
                            if musicname:
                                print(musicname.group(0)[1:-5])
                    else:
                        print(item.a.string)
            except:
                continue
            try:
                if item.b.string != None:
                    for i in item.find_all('td'):
                        pattern = '>(.*?)<span'
                        musicname = re.search(pattern,str(i))
                        if musicname:
                            print(musicname.group(0)[1:-5])
                        print('/n')
            except:
                continue
'''