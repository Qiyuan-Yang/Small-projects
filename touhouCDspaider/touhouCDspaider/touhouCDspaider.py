import requests
from bs4 import BeautifulSoup
import bs4
import re
import time
 
def Gethtmltext(url, code="utf-8"): 
    #a simple modul to get html text
    try:
        r = requests.get(url,headers = {'user-agent':'Mozilla/5.0'})
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''

def Getalbumhtml(url,startalbum = '"Activity" Case：01 -Graveyard Memory-'): 
    #to get the html text in album pages
    html = Gethtmltext(url+startalbum)
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('div'):
        if tag.get('class') == ['mw-category-generated']:
            return(tag)

def Generatealbumlist(albumlist,startalbum = '"Activity" Case：01 -Graveyard Memory-'):
    #to get album names in album pages
    for title in Getalbumhtml(url,startalbum).find_all('a'):
        if title.string == '上一页' or title.string == '下一页':
            continue
        else:
            albumlist.append(title.string)

def Exportalbuminfo(albumlist,startalbum = '"Activity" Case：01 -Graveyard Memory-'):
    #actually the main function
    mode = eval(input('模式1 为 获取专辑列表 模式2 为 获取单曲列表\n'))
    Generatealbumlist(albumlist,startalbum)
    f = open('C:/localdata.txt','w',encoding='utf-8')
    number = 0
    #an additional modul to make a prograss bar
    count = 0
    scale = 50
    start = time.perf_counter()
    print("执行开始".center(scale//2, "-"))
    #try to traverse all album pages
    while len(albumlist) > 1:
        a = '*' * int(count/1.1)
        b = '.' * (scale - int(count/1.1))
        c = (int(count/1.1)/scale)*100
        dur = time.perf_counter() - start
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
        count += 1
        #try to get all vocal/music in each album
        for i in range(len(albumlist)):
            if i != 0 or startalbum == '"Activity" Case：01 -Graveyard Memory-':
                if mode == 1:
                    f.write(albumlist[i])
                    f.write('\n')
                else:
                    Getalbuminfo(albumlist[i],f)
        startalbum = albumlist[-1]
        albumlist = []
        Generatealbumlist(albumlist,startalbum)
    f.close()
    #the additional modul of prograss bar to make sure it stop at 100%
    a = '*' * 50
    b = '.' * (scale - 50)
    c = (50/scale)*100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
    print("\n"+"执行结束".center(scale//2,'-'))

def Getalbuminfo(albumname,filename):
    #actually the most usful function
    #it contain the function to get all vocal/music and the function to make a output
    albumurl = 'https://thwiki.cc/'
    html = Gethtmltext(albumurl+albumname)
    soup = BeautifulSoup(html, 'html.parser')
    text = []
    musicinfo = []
    musicinfo.append(albumname)
    for tag in soup.find_all('table'):
        if tag.get('class') == ['wikitable', 'musicTable']:
            for item in tag.find_all('tr'):
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
                        else:
                            continue
                        if musicinfo[-1] != albumname and musicinfo[-2] != albumname:
                            for position in range(len(musicinfo)):
                                filename.write(musicinfo[position])
                                if position == len(musicinfo) - 1:
                                    filename.write('\n')
                                else:
                                    filename.write(',')
                            musicinfo = []
                            musicinfo.append(albumname)
                        else:
                            continue

url = 'https://thwiki.cc/index.php?title=分类:同人专辑&pagefrom='
albumlist = []
choice = input('是否定义起始专辑\n')
if choice == 'yes':
    startalbum = input('输入起始专辑\n')
    Exportalbuminfo(albumlist,startalbum)
else:
    Exportalbuminfo(albumlist)

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