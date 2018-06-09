import requests
import time
from bs4 import BeautifulSoup, NavigableString
import time
import json
import re

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

def convert_open_hours(element):
    childa = '～'
    hours = {}
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Initialize hours
    for d in week_days:
        hours[d] = []

    for duration in element.childGenerator():
        if duration.name == 'br':
            continue

        pattern_childa = r'\[.' + childa + '.\]'
        pattern_dot = r'\[.・.\]'
        pattern_hour = r'\d+:\d+' + childa + '翌?\d+:\d+'
        
        duration = duration.string
        matched_childa = re.findall(pattern_childa, duration)
        matched_dot = re.findall(pattern_dot, duration)
        matched_hour = re.findall(pattern_hour, duration)
        if not matched_hour:
            continue
        print(matched_childa)
        print(matched_dot)
        print(matched_hour)
        
        # if working hours are the same accross days
        if (not matched_childa) and (not matched_dot):
            matched_hour = matched_hour[0]
            start_time, finish_time = matched_hour.split(childa)
            value = {'start': start_time, 'finish': finish_time}
            for d in week_days:
                hours[d].append(value)

        #if matched_childa:
        #    days = list('月火水木金土日')
        #    start_day, finish_day = matched_childa[0][1:-1].split(childa)
        #    print(start_day, finish_day)
        #    working_days = days[days.index(start_day), days.index(finish_day)]
        #    print(working_days)
    return hours

for i, row in enumerate(restaurant_links):
    url = row['url']
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    tds = soup.find_all('td')
    name = tds[1].text.strip()
    zipcode, address = convert_address(tds[3].text)
    tel = tds[5].text
    print(name)
    print(tds[7])
    opens = convert_open_hours(tds[7])
    print(opens)
    holidays = tds[9].text
    access = tds[11].text
    opened_in = tds[13].text
    menu = tds[15].text
    # get coordination
    soup_geo = BeautifulSoup(requests.get('http://www.geocoding.jp/api/?v=1.1&q='+address).content, 'xml')

    data.append({
        'id': i,
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
else:
    jsondata = {'restaurants': data}

with open('restaurants.json', 'wb') as f:
    f.write(json.dumps(jsondata, ensure_ascii = False).encode("utf8"))
