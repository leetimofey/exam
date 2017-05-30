from bs4 import BeautifulSoup
from firebase import firebase
import requests

firebase_url = "https://exam1-b2d03.firebaseio.com/"

class Inform:
    zag = ""
    IMGS = ""
    TEXTS = ""
    author = ""

    def __init__(self, zag, IMGS, TEXTS, author):
        self.zag = zag
        self.IMGS = IMGS
        self.TEXTS = TEXTS
        self.author = author

allInform = []
IMGS = []
TEXTS = []

urls = ['https://izvestia.ru/news/716546', "https://izvestia.ru/news/716549", "https://izvestia.ru/news/716534", "https://izvestia.ru/news/710558", "https://izvestia.ru/news/716531", "https://izvestia.ru/news/716528", "https://izvestia.ru/news/715529", "https://izvestia.ru/news/714908", "http://izvestia.ru/news/719261", "http://izvestia.ru/news/719153"]
for url in urls:
    html_doc = requests.get(url).text

    soup = BeautifulSoup(html_doc, 'html5lib')
    zagol = soup.findAll("div", {'class': 'article-content__head'})
    for item in zagol:
        zag = item.find('h1', {'class': 'article-content__title'}).text
    table = soup.findAll("div", {"class": "page__content page__content_indent"})
    for item in table:
        imgs_url = item.findAll('img')
        for i in imgs_url:
            a = i.get('src')
            IMGS.append(a)
    texts = soup.findAll("div", {'class': 'page__content page__content_indent'})
    for item in texts:
        info = item.findAll('p')
        for i in info:
            a = i.text
            TEXTS.append(a)
    authors = soup.findAll('div', {'class': 'article-content__data'})
    for item in authors:
        author=item.find('a', {'class': 'article-content__data-authors'}).text

    allInform.append(Inform(zag, IMGS, TEXTS, author))

db = firebase.FirebaseApplication(firebase_url)

for user in allInform:
    db.post("/texts", user.__dict__)