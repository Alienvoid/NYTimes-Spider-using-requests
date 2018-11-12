import requests
import json
from bs4 import BeautifulSoup
import os
PATH = "./"
URLLIST_PATH = "./urlList.txt"
with open(PATH+r"cookie.txt", "r") as file:
    cookie = file.read()
cookie = json.loads(cookie)[-1]
s = requests.Session()
s.cookies = cookie
s.keep_alive = False
requests.adapters.DEFAULT_RETRIES = 9999
with open(URLLIST_PATH, "r") as f:
    urlList = eval(f.read())
counter = 0  # If your downloading stops due to the network, just modify the counter.
def get_author(soup):
    author_nominator_0 = soup.find("meta", attrs={"name": "author"})
    author_nominator_1 = soup.find("meta", attrs={"name": "cre"})
    if author_nominator_0 is not None:
        return author_nominator_0["content"]
    elif author_nominator_1 is not None:
        return author_nominator_1["content"]
    else:
        return "New York Times Editor"
def get_title(soup):
    try:
        return soup.find("meta", attrs={"name": "hdl"})["content"]
    except:
        title = url.split(r"/")[-1][:-6]
        return " ".join([word.capitalize() for word in title.split("-")])
def get_date(soup):
    try:
        return soup.find("meta", attrs={"name": "pdate"})["content"]
    except:
        return "NOT FOUND"
def get_key_words(soup):
    kw_1 = soup.find("meta", attrs={"name": "keywords"})
    kw_2 = soup.find("meta", attrs={"name": "news_keywords"})
    if kw_1 is not None:
        return kw_1["content"]
    elif kw_2 is not None:
        return kw_2["content"]
    else:
        return "NOT FOUND"
def get_description(soup):
    try:
        return soup.find("meta", attrs={"name": "description"})["content"].replace(r"\n", "").replace(r"<p>", "")
    except:
        return "NOT FOUND"
 # If your downloading stops due to the network, just slice urlList. e.g. urlList[56:], the number should be the same as counter.
for url in urlList:
    print("Parsing "+url)
    counter+=1
    doc = requests.get(url).text
    soup = BeautifulSoup(doc, "lxml")
    title = get_title(soup)
    print(title)
    author = get_author(soup)
    publicated_time = get_date(soup)
    path = "/Article/NYTimes"+str(counter)+".txt"
    media = "New York Times"
    key_words = get_key_words(soup)
    description = get_description(soup)
    # DEAL WITH THE ARTICLE
    content = "NOT FOUND"
    QAselector = "div.entry-content"
    article_selector_0 = soup.find_all("div", attrs={"class":"StoryBodyCompanionColumn"})
    article_selector_1 = soup.find_all("p", attrs={"class": "story-body-text story-content"})
    article_selector_2 = soup.find_all("p", attrs={"class":"story-body-text"})
    article_selector_3 = soup.find_all("p", attrs={"itemprop": "articleBody"})
    if len(soup.select(QAselector))!=0:
        raw_content = soup.find_all("p", attrs={"class":"story-body-text"})
        if len(raw_content)==0:
            content = json.dumps({"ScreenshotURL":soup.select(QAselector)[0].text})
            print("QA SELECTOR")
        else:
            content = "".join([tag.text for tag in soup.find_all("p", attrs={"class":"story-body-text"})])
            print("DEFAULT SELECTOR")
    elif len(article_selector_0)!=0:
        content = "".join([tag.text for tag in article_selector_0])
        print("SELECTOR 0")
    elif len(article_selector_1)!=0:
        content = "".join([tag.text for tag in article_selector_1])
        print("SELECTOR 1")
    elif len(article_selector_2)!=0:
         content = "".join([tag.text for tag in article_selector_2])
         print("SELECTOR 2")
    elif len(article_selector_3) != 0:
        content = "".join([tag.text for tag in article_selector_3])
        print("SELECTOR 3")
    if "Digitized text of this article is not available" in content:
        content = "MEET UNEXPECTED WEBSITE, URL:"+url
    raw_dict = {"Title": title,
                 "Path": path,
                 "Publicated_time": publicated_time,
                 "Author": author,
                 "Url": url,
                 "Keywords": key_words,
                 "Description": description,
                 "Media": media}
    index_content = json.dumps(raw_dict)
    with open(PATH+r"Article_Index/NewYorkTimes" + str(counter) + ".txt", "w",
                 encoding='utf-8') as index_file:
        index_file.write(index_content)
        index_file.close()
    with open(PATH+r"Article/NewYorkTimes" + str(counter) + ".txt", "w",
                 encoding='utf-8') as index_file:
        index_file.write(content)
        index_file.close()