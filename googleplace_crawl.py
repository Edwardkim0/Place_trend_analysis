from urllib.request import urlopen
import scrapy
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup as bs
import urllib.parse

# 교보문고의 베스트셀러 웹페이지를 가져옵니다.

search_place = '홍대'
search_word = search_place + '딸기 타르트'
base_url = 'https://www.google.com/maps/'
driver = webdriver.Chrome()

driver.get(base_url)
search_window = driver.find_element_by_xpath('''/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div/div[3]/div/input[1]''')
search_window.send_keys(search_word)
enterkey = driver.find_element_by_xpath('''/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button''')
enterkey.click()

html = urlopen(driver.current_url)

bsObject = bs(html, "html.parser")

# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
place_page_urls = []
for cover in bsObject.select('div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div > div.section-result-content > div.section-result-text-content > div > span.section-result-location'):
    link = cover.select('a')[0].get('href')
    place_page_urls.append(link)
'//*[@id="pane"]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/span/span[2]'
# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.

# for i in range(1,)
'//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[3]/div[1]/div[1]/div[2]/span[6]'
'//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[5]/div[1]/div[1]/div[2]/span[6]'
'//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[7]/div[1]/div[1]/div[2]/span[6]'
'//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[41]/div[1]/div[1]/div[2]/span[6]'

'//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[41]/div[1]/div[1]/div[1]/div[1]/div[2]/h3/span'

for index, place_page_url in enumerate(place_page_urls):
    html = urlopen(place_page_url)
    bsObject = bs(html, "html.parser")
    title = bsObject.find('meta', {'property':'rb:itemName'}).get('content')
    author = bsObject.select('span.name a')[0].text
    image = bsObject.find('meta', {'property':'rb:itemImage'}).get('content')
    url = bsObject.find('meta', {'property':'rb:itemUrl'}).get('content')
    originalPrice = bsObject.find('meta', {'property': 'rb:originalPrice'}).get('content')
    salePrice = bsObject.find('meta', {'property':'rb:salePrice'}).get('content')

    print(index+1, title, author, image, url, originalPrice, salePrice)