from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re



def getHtmlText(url, loadmore = False, waittime = 2):
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

word = input()
url = "https://fanyi.baidu.com/#en/zh/" + word
text = getHtmlText(url)
soup = BeautifulSoup(text,'html.parser')
for div in soup.div:
    try:
        if div.attrs['class'] == ['main', 'main-outer']:
            pattern = '<p class="entry-d f-gap-top">(.*?)<br'
            for trans in re.findall(pattern,str(div)):
                subpattern = 'span>(.*?)<br'
                subtrans = re.findall(subpattern,str(trans))
                if subtrans:
                    print(subtrans)
                elif trans:
                    print('\n'*2)
                    print(trans)
    except:
        continue