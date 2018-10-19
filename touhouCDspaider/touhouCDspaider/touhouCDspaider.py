import requests
from bs4 import BeautifulSoup
import bs4
import re
import time
from multiprocessing import Pool
 
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
    for title in getAlbumHtml('https://thwiki.cc/index.php?title=分类:同人专辑&pagefrom=',startAlbum).find_all('a'):
        if title.string == '上一页' or title.string == '下一页':
            continue
        else:
            albumList.append(title.string)

def exportAlbumInfo(albumList = [],startAlbum = '"Activity" Case：01 -Graveyard Memory-',mode = 0):
    #actually the main function
    generateAlbumList(albumList,startAlbum)
    if mode == 2:
        f = open('C:/musicLocalData.txt','w',encoding='utf-8')
    else:
        f = open('C:/albumLocalData.txt','w',encoding='utf-8')
    #an additional modul to make a prograss bar
    count = 0
    scale = 50
    start = time.perf_counter()
    print("执行开始 start processing".center(scale//2, "-"))
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
    print("\n"+"执行结束 end processing".center(scale//2,'-'))

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

def searchSingleInfo(file,single,lang = '中文'):
    f = open(file,encoding = 'UTF-8')
    for line in f.readlines():
        info = line.split(',')
        if single in info[1]:
            if lang == '中文':
                print('所属专辑：{} \n包含原曲及原曲来源：{}'.format(info[0],info[1:-1]))
            elif lang == 'English':
                print('the album it belongs to：{} \nthe ogmusic it contains：{}'.format(info[0],info[1:-1]))

def searchAlbumInfo(file,album,lang):
    f = open(file,encoding = 'UTF-8')
    for line in f.readlines():
        info = line.split(',')
        if single in info[0]:
            if lang == '中文':
                print('包含单曲：{} \n原曲及原曲来源：{}'.format(info[1],info[1:-1]))
            elif lang == 'English':
                print('the singles it contains：{} \nthe ogmusic it contains：{}'.format(info[1],info[1:-1]))

def checkUpdate(file,*lang):
    f = open(file,encoding = 'UTF-8')
    txt = f.read()
    txt = txt.split('\n')
    output = open('C:/updateList.txt','w',encoding = 'UTF-8')
    startAlbum = '"Activity" Case：01 -Graveyard Memory-'
    count = 0
    scale = 50
    start = time.perf_counter()
    print("执行开始 start processing".center(scale//2, "-"))
    albumList = []
    updateList = []
    #start = time.perf_counter()
    generateAlbumList(albumList)
    while len(albumList) > 1:
        for i in range(len(albumList)):
            if i != 0 or startAlbum == '"Activity" Case：01 -Graveyard Memory-':
                if albumList[i] in txt[count:len(txt)]:
                    count += 1
                    bar = int(scale*count/len(txt))
                    a = '*' * bar
                    b = '.' * (scale - bar)
                    c = (count/len(txt))*100
                    dur = time.perf_counter() - start
                    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
                else:
                    output.write(albumList[i])
                    output.write('\n')
                    updateList.append(albumList[i])
        startAlbum = albumList[-1]
        albumList = []
        generateAlbumList(albumList,startAlbum)
    #the additional modul of prograss bar to make sure it stop at 100%
    a = '*' * 50
    b = '.' * 0
    c = 100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
    print("\n"+"执行结束 end processing".center(scale//2,'-'))
    if updateList == []:
        if lang == '汉语':
            print('无需更新')
        else:
            print('No update')
    else:
        if lang == '汉语':
            print('检查到更新')
        else:
            print('Need update')
    f.close()
    output.close()
    

def getUpdate(file):
    input = open(file,encoding = 'UTF-8')
    txt = input.read()
    txt = txt.split('\n')
    count = 0
    scale = 50
    start = time.perf_counter()
    print("执行开始 start processing".center(scale//2, "-"))
    f = open('C:/musicLocalData.txt','a',encoding='utf-8')
    for album in txt:
        getAlbumInfo(album,f)
        count += 1
        bar = int(scale*count/len(txt))
        a = '*' * bar
        b = '.' * (scale - bar)
        c = (count/len(txt))*100
        dur = time.perf_counter() - start
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
    f.close()
    input.close()
    print('更新专辑信息 updating album data')
    exportAlbumInfo(mode = 1)
    print('\n')

def main():
    lang = input('汉语请输入1 for English please key in 2\n')
    if lang == '1':
        ending = '否'
        while ending in '不否':
            module = input('检查更新请输入1 获取更新请输入2 获取单曲信息请输入3 匹配原曲请输入4 退出请输入0\n')
            #if module == '1':
            #    exportAlbumInfo(mode = 1)
            #elif module == '2':
            #    exportAlbumInfo(mode = 2)
            if module == '1':
                checkUpdate('C:/albumLocalData.txt','汉语')
            elif module == '2':
                getUpdate('C:/updateList.txt')
            elif module == '3':
                single = input('请输入单曲名\n')
                searchSingleInfo('C:/musicLocalData.txt',single)
            elif module == '4':
                ogmusic = input('请输入原曲名\n')
                ogmusicMatch('C:/musicLocalData.txt',ogmusic)
            elif module == 'advance':
                module = input('获取专辑列表请输入1 获取单曲信息请输入2\n')
                if module == '1':
                    exportAlbumInfo(mode = 1)
                elif module == '2':
                    exportAlbumInfo(mode = 2)
            else:
                break
            ending = input('结束？\n')
            if ending == '':
                break
    if lang == '2':
        ending = 'no'
        while ending in 'not':
            module = input("key in '1' for checking update\nkey in '2' for getting update\nkey in '3' for getting single's info\nkey in '4' for matching ogmusic\nkey in '0' for exit\n")
            #if module == '1':
            #    exportAlbumInfo(mode = 1)
            #elif module == '2':
            #    exportAlbumInfo(mode = 2)
            if module == '1':
                checkUpdate('C:/albumLocalData.txt','English')
            elif module == '2':
                getUpdate('C:/updateList.txt')
            elif module == '3':
                single = input("please key in single's name\n")
                searchSingleInfo('C:/musicLocalData.txt',single)
            elif module == '4':
                ogmusic = input('pleaes key in ogmusic name\n')
                ogmusicMatch('C:/musicLocalData.txt',ogmusic)
            elif module == 'advance':
                module = input('获取专辑列表请输入1 获取单曲信息请输入2\n')
                if module == '1':
                    exportAlbumInfo(mode = 1)
                elif module == '2':
                    exportAlbumInfo(mode = 2)
            else:
                break
            ending = input('exit?\n')
            if ending == '':
                break

if __name__ == '__main__':
    main()