import requests
import time
from bs4 import BeautifulSoup
import time
import json

top_url = 'http://xn--4dkp5a8a4562a1c2fvhm.com/shoplist'

res = requests.get(top_url)
soup = BeautifulSoup(res.content, 'lxml')
article = soup.find(attrs={'class': 'article'})
rows =  article.find_all('a')
restaurant_links = [{'url':row.get('href'), 'name': row.text} for row in rows]

data = []
def convert_address(address_text):
    address_text = address_text.replace('〒', '').strip()
    if address_text[0].isdigit():
        zipcode, address = address_text.split(' ', 1)
    else:
        zipcode = ''
        address = address_text
    return zipcode, address

for row in restaurant_links:
    url = row['url']
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    tds = soup.find_all('td')
    name = tds[1].text.strip()
    zipcode, address = convert_address(tds[3].text)
    tel = tds[5].text
    opens = tds[7].text
    holidays = tds[9].text
    access = tds[11].text
    opened_in = tds[13].text
    menu = tds[15].text

    # get coordination
    soup_geo = BeautifulSoup(requests.get('http://www.geocoding.jp/api/?v=1.1&q='+address).content, 'xml')
    print(float(soup_geo.lat.text))

    data.append({
        'name': name,
        'zipcode': zipcode,
        'address': address.strip(),
        'tel': tel,
        'opens': opens,
        'holidays': holidays,
        'access': access,
        'opened_in': opened_in,
        'menu': menu,
        'coordinate': {'lat': float(soup_geo.lat.text), 'lng': float(soup_geo.lng.text)}
        })
    print(data)
    time.sleep(3)
else:
    jsondata = {'restaurants': data}

with open('restaurants.json', 'wb') as f:
    f.write(json.dumps(jsondata, ensure_ascii = False).encode("utf8"))
