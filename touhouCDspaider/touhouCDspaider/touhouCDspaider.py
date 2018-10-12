import requests
from bs4 import BeautifulSoup
import bs4
import re
import time
 
def getHtmlText(url, code="utf-8"): 
    #a simple modul to get html text
    try:
        r = requests.get(url,headers = {'user-agent':'Mozilla/5.0'})
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''

def getAlbumHtml(url,startAlbum = '"Activity" Case：01 -Graveyard Memory-'): 
    #to get the html text in album pages
    html = getHtmlText(url+startAlbum)
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('div'):
        if tag.get('class') == ['mw-category-generated']:
            return(tag)

def generateAlbumList(albumList,startAlbum = '"Activity" Case：01 -Graveyard Memory-'):
    #to get album names in album pages
    for title in getAlbumHtml(url,startAlbum).find_all('a'):
        if title.string == '上一页' or title.string == '下一页':
            continue
        else:
            albumList.append(title.string)

def exportAlbumInfo(albumList,startAlbum = '"Activity" Case：01 -Graveyard Memory-'):
    #actually the main function
    mode = eval(input('模式1 为 获取专辑列表 模式2 为 获取单曲列表\n'))
    generateAlbumList(albumList,startAlbum)
    f = open('C:/localdata.txt','w',encoding='utf-8')
    number = 0
    #an additional modul to make a prograss bar
    count = 0
    scale = 50
    start = time.perf_counter()
    print("执行开始".center(scale//2, "-"))
    #try to traverse all album pages
    while len(albumList) > 1:
        a = '*' * int(count/1.1)
        b = '.' * (scale - int(count/1.1))
        c = (int(count/1.1)/scale)*100
        dur = time.perf_counter() - start
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
        count += 1
        #try to get all vocal/music in each album
        for i in range(len(albumList)):
            if i != 0 or startAlbum == '"Activity" Case：01 -Graveyard Memory-':
                if mode == 1:
                    f.write(albumList[i])
                    f.write('\n')
                else:
                    getAlbumInfo(albumList[i],f)
        startAlbum = albumList[-1]
        albumList = []
        generateAlbumList(albumList,startAlbum)
    f.close()
    #the additional modul of prograss bar to make sure it stop at 100%
    a = '*' * 50
    b = '.' * (scale - 50)
    c = (50/scale)*100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
    print("\n"+"执行结束".center(scale//2,'-'))

def getAlbumInfo(albumName,fileName):
    #actually the most usful function
    #it contain the function to get all vocal/music and the function to make a output
    albumUrl = 'https://thwiki.cc/'
    html = getHtmlText(albumUrl+albumName)
    soup = BeautifulSoup(html, 'html.parser')
    text = []
    musicInfo = []
    musicInfo.append(albumName)
    for tag in soup.find_all('table'):
        if tag.get('class') == ['wikitable', 'musicTable']:
            for item in tag.find_all('tr'):
                try:
                    a = item.b.string
                    if a in '0102030405060708091121314151617181922324252627282933435363738394454647484955657585966768697787988990':
                        if item.a.string == None:
                            for j in item.find_all('td'):
                                pattern = '>(.*?)<span'
                                musicName = re.search(pattern,str(j))
                                if musicName:
                                    musicName = musicName.group(0)[1:-5]
                                    if '\u3000' in musicName:
                                        musicName = musicName.replace('\u3000',' ')
                                    musicInfo.append(musicName)
                        else:
                            if '\u3000' in item.a.string:
                                item.a.string = item.a.string.replace('\u3000',' ')
                            musicInfo.append(item.a.string)
                except AttributeError:
                    for td in item.find_all('td'):
                        if td.string == '原曲':
                            for ogmusic in item.find_all('a'):
                                if ogmusic.string != None:
                                    if '\u3000' in ogmusic.string:
                                        ogmusic.string = ogmusic.string.replace('\u3000',' ')
                                        musicInfo.append(ogmusic.string)
                                    else:
                                        musicInfo.append(ogmusic.string)
                        else:
                            continue
                        if musicInfo[-1] != albumName and musicInfo[-2] != albumName:
                            for position in range(len(musicInfo)):
                                fileName.write(musicInfo[position])
                                if position == len(musicInfo) - 1:
                                    fileName.write('\n')
                                else:
                                    fileName.write(',')
                            musicInfo = []
                            musicInfo.append(albumName)
                        else:
                            continue

def ogmusicMatch(file,ogmusic,lang = '中文'):
    count = 0
    f = open(file,encoding = 'UTF-8')
    for line in f.readlines():
        info = line.split(',')
        if ogmusic in info:
            count += 1
            if lang == '中文':
                print('第{}首'.format(count),end = ':')
                print('\n专辑名：{} \n单曲名：{}'.format(info[0],info[1]))
            elif lang == 'English':
                print('The No.{}'.format(count),end = ':')
                print('\nalbum name:{} \nsingle name:{}'.format(info[0],info[1]))

def getSingleInfo(file,single,lang = '中文'):
    f = open(file,encoding = 'UTF-8')
    for line in f.readlines():
        info = line.split(',')
        if single in info[1]:
            if lang == '中文':
                print('所属专辑：{} \n包含原曲及原曲来源：{}'.format(info[0],info[1:-1]))
            elif lang == 'English':
                print('the album it belongs to：{} \nthe ogmusic it contains：{}'.format(info[0],info[1:-1]))

def getAlbumInfo(file,album,lang):
    f = open(file,encoding = 'UTF-8')
    for line in f.readlines():
        info = line.split(',')
        if single in info[0]:
            if lang == '中文':
                print('包含单曲：{} \n原曲及原曲来源：{}'.format(info[1],info[1:-1]))
            elif lang == 'English':
                print('the singles it contains：{} \nthe ogmusic it contains：{}'.format(info[1],info[1:-1]))

def main():

url = 'https://thwiki.cc/index.php?title=分类:同人专辑&pagefrom='
albumlist = []
choice = input('是否定义起始专辑\n')
if choice == 'yes':
    startalbum = input('输入起始专辑\n')
    exportAlbumInfo(albumlist,startalbum)
else:
    exportAlbumInfo(albumlist)

