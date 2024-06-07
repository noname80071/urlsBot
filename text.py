from bs4 import BeautifulSoup
import requests

url = 'https://t.me/Chychelo1'

st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
headers = {
    "Accept": st_accept,
    "User-Agent": st_useragent
}
req = requests.get(url, headers)
src = req.text

soup = BeautifulSoup(src, 'html.parser')
# считываем заголовок страницы
divs = soup.find_all('div')
for div in divs:
    print(1)
    print(div.get('class'))
    if div.get('class') == ['tgme_page_photo']:
        p