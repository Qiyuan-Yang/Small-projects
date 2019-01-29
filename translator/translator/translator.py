from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re



def getHtmlText(url, loadmore = False, waittime = 1):
    path = 'C:\\Users\\yangq\\Downloads\\chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(path,options = chrome_options)
    browser.get(url)
    time.sleep(waittime)
    if loadmore:
        while True:
            try:
                next_button = browser.find_element_by_class_name("more")
                next_button.click()
                time.sleep(waittime)
            except:
                break
    html = browser.page_source
    browser.quit()
    return html

def selector(origin,tag,contain):
    for div in origin:
        try:
            if div.attrs[tag] == contain:
               return div
        except:
            continue


def oxford(translation,result):
    translation = str(translation)
    idiomPat = '<div class="entry-idg f-overflow-hidden entry-idg-outdent(.*?)</div>'
    for idiomTrans in re.findall(idiomPat,translation):
        if idiomTrans:
            idiom = re.findall('<p class="idg-id">(.*?)</p>',idiomTrans)
            trans = re.findall('   (.*?) ',idiomTrans)
            result.append(' -' + idiom[0] + trans[0])
            translation = translation.replace(idiomTrans,'')
    wordPat = '<p class="entry-d f-gap-top">   (.*?) '
    for wordTrans in re.findall(wordPat,translation):
        if wordTrans:
            result.append(wordTrans)
            

retry = 1
while retry:
    result = []
    word = input('请输入单词\n')
    url = "https://fanyi.baidu.com/#en/zh/" + word
    text = getHtmlText(url)
    soup = BeautifulSoup(text,'html.parser')
    translation = selector(soup.div,'class',['main', 'main-outer'])
    translation = translation.div.div.div
    translation = selector(translation,'class',['trans-other-wrap', 'clearfix'])
    translation = selector(translation,'class',['trans-left'])
    count = 0
    for div in translation:
        count += 1
        if count == 6:
            translation = div
    soup = BeautifulSoup(str(translation),'html.parser')
    count = 0
    for tag in soup.div:
        count += 1
        if count == 4:
            translation = tag
    count = 0
    for tag in translation:
        count += 1
        if count == 4:
            translation = tag
    oxford(translation,result)
    result.append(word)
    result.reverse()
    result = '；'.join(result)
    result = result.replace('；','',1)
    print(result)
    save = input('是否保存\n')
    if save:
        f = open('D:/translation.txt','a')
        f.write(result+'\n')
        f.close()
    retry = input('是否继续\n')
