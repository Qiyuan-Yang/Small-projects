from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re



def getHtmlText(url, loadmore = False, waittime = 2):
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


def oxford(translation,results):
    translation = str(translation)
    idiomPat = '<div class="entry-idg f-overflow-hidden entry-idg-outdent(.*?)</div>'
    for idiomTrans in re.findall(idiomPat,translation):
        if idiomTrans:
            idiom = re.findall('<p class="idg-id">(.*?)</p>',idiomTrans)
            trans = re.findall('   (.*?) ',idiomTrans)
            result = ' -' + idiom[0] + trans[0]
            if result in results:
                continue
            else:
                results.append(result)
            translation = translation.replace(idiomTrans,'')
    wordPat = '<p class="entry-d f-gap-top">   (.*?) '
    for wordTrans in re.findall(wordPat,translation):
        if wordTrans:
            results.append(wordTrans)

def collins(translation,results):
    translation = str(translation)
    wordPat = '<span class="mean-tran">(.*?)</span>'
    for wordTrans in re.findall(wordPat,translation):
        if wordTrans:
            results.append(wordTrans)
            

retry = 1
while retry:
    results = []
    word = input('请输入单词\n')
    url = "https://fanyi.baidu.com/#en/zh/" + word
    text = getHtmlText(url)
    soup = BeautifulSoup(text,'html.parser')
    oxford(soup,results)
    if results:
        results.append(word)
        results.reverse()
        results = '；'.join(results)
        results = results.replace('；','',1)
        print(results)
    else:
        collins(soup,results)
        results.append(word)
        results.reverse()
        results = '；'.join(results)
        results = results.replace('；','',1)
        print(results)
    save = input('是否保存\n')
    if save:
        f = open('D:/translation.txt','a')
        f.write(results+'\n')
        f.close()
    retry = input('是否继续\n')
