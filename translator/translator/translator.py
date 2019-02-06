from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re



def getHtmlText(url, loadmore = False, waittime = 1):
    path = 'C:\\Users\\von SolIII\\Downloads\\chromedriver.exe'
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
    idiomPat = '<div class="entry-idg f-overflow-hidden(.*?)</div>'
    for idiomTrans in re.findall(idiomPat,translation):
        if idiomTrans:
            idiom = re.findall('<p class="idg-id">(.*?)</p>',idiomTrans)
            for trans in re.findall('   (.*?) ',idiomTrans):
                if trans:
                    result = ' -' + idiom[0] + trans
            if result in results:
                continue
            else:
                results.append(result)
            translation = translation.replace(idiomTrans,'')
    wordPat = '<p class="entry-d f-gap-top">(.*?)</p>'
    for wordTrans in re.findall(wordPat,translation):
        if wordTrans:
            pat = '   (.*?) <br'
            wordTrans = re.findall(pat,wordTrans)
            if 'span' in wordTrans[0]:
                wordTrans[0] = wordTrans[0]+' '
                wordTrans = re.findall('   (.*?) ',wordTrans[0])
            results.append(wordTrans[0])

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
    oxford(text,results)
    if results:
        results.append(word)
        results.reverse()
        results = '；'.join(results)
        results = results.replace('；','',1)
        print(results)
    else:
        collins(text,results)
        results.append(word)
        results.reverse()
        results = '；'.join(results)
        results = results.replace('；','',1)
        print(results)
    save = input('是否保存\n')
    if save:
        f = open('C:/translation.txt','a')
        f.write(results+'\n')
        f.close()
