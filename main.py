import requests
import urllib.request
import os
import random
from bs4 import BeautifulSoup


def get_headers():
    headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 "
        "(KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) "
        "Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.17 Safari/537.36"
    ]

    return {"User-Agent": random.choice(headers)}


def get_ips():

    ips = [
        '183.95.80.102:8080',
        '123.160.31.71:8080',
        '115.231.128.79:8080',
        '166.111.77.32:80',
        '43.240.138.31:8080',
        '218.201.98.196:3128'
    ]

    return {'http': random.choice(ips)}


class KKday:

    def __init__(self, city):
        self.city = city

    def get_kkday(self):
        if not self.city:
            return []

        url = f"https://www.kkday.com/zh-tw/product/ajax_productlist/?country=&city=&keyword={self.city}&availstartdate=&availenddate=&cat=&time=&glang=&sort=rdesc&page=1&row=10&fprice=*&eprice=*&precurrency=TWD"
        re = requests.get(url)
        datas = re.json()['data']

        results = []  # return

        for data in datas:
            title = data['name']
            link = data['url']
            rate = data['rating_star']
            price = data['price']

            results.append({
                'title': title, 'link': link, 'rate': rate, 'price': price
            })

        return results


class Dcard:

    def __init__(self, type_):
        self.type_ = type_

    def get_images(self):

        url = f"https://www.dcard.tw/f/{self.type_}"
        re = requests.get(url)
        soup = BeautifulSoup(re.text)
        articles = soup.find_all('img', class_='sc-2rneb0-0 imygTk tgn9uw-7 mMUlZ')

        results = []

        for article in articles:
            results.append(article['src'])

        return results


class Icook:

    def __init__(self, ingredients):
        self.ingredients = ingredients

    def get_recipes(self):

        url = f"https://icook.tw/search/%E9%A3%9F%E6%9D%90%EF%BC%9A{self.ingredients}/"
        re = requests.get(url, headers=get_headers(), proxies=get_ips())
        soup = BeautifulSoup(re.text)
        datas = soup.find_all('li', class_='browse-recipe-item')
        results = []

        for data in datas:
            name = data.find('h2', class_='browse-recipe-name').text
            name = name.strip()
            ingredients = data.find('p', class_='browse-recipe-content-ingredient').text
            ingredients = ingredients.strip()
            link = data.find('a', class_='browse-recipe-link')['href']
            link = f'https://icook.tw{link}'

            results.append({
                'name': name, 'ingredients': ingredients, 'link': link
            })

        return results


def download(urls, path):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    if not os.path.exists(path):
        os.mkdir(path)

    for url in urls:
        name = url.split('/')[-1]
        urllib.request.urlretrieve(url, path + name)


if __name__ == '__main__':
    kkday = KKday('高雄')
    print(kkday.get_kkday())

    dcard = Dcard('pet')
    print(dcard.get_images())

    icook = Icook('雞')
    print(icook.get_recipes())

