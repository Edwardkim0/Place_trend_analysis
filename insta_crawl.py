from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from urllib.request import Request, urlopen
from time import sleep
import pandas as pd
from multiprocessing import Pool, Value, freeze_support
import parmap
from collections import defaultdict

num = 0

web_driver_path="C:\\project\\code\\ai_company_evaluatuion\\chromedriver_win32\\chromedriver.exe"


def crawling(driver,x,save_name):
    driver.get('https://www.instagram.com/p' + x)
    postDict = {}

    userClass = driver.find_element_by_xpath("//div[contains(@class, 'e1e1d')]")
    user = userClass.find_element_by_css_selector('a').text
    likeNum = '0'
    try:
        likeNumClass = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]/div/div/button""")
        likeNum = likeNumClass.find_element_by_css_selector('span').text
        print (likeNum)
    except:
        print(f'likeNumClass error')
    postDict["likeNum"] = likeNum

    writetime = '0'
    try:
        timeClass = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/div[1]/article/div[2]/div[2]/a/time""")
        writetime = timeClass.get_attribute('datetime')
        print (writetime)
    except:
        print(f'timeClass error')
    postDict["writetime"] = writetime

    hasLocation = '0'
    try:
        # locationClass = self.driver.find_elements_by_xpath("//a[contains(@class, '_6y8ij')]")
        # locationClass = driver.find_elements_by_xpath("//a[contains(@class, 'O4GlU')]")
        locationClass = driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[2]/div[2]/a")
        if len(locationClass) > 0:
            hasLocation = locationClass[0].text
    except:
        print("locationClass error")
    postDict["hasLocation"] = hasLocation

    AtUserLinkList = []
    hashTagList = []
    ContentList = []
    # CommetClass =  self.driver.find_element_by_xpath("//ul[contains(@class, '_b0tqa')]")
    # CommetClassList = CommetClass.find_elements_by_xpath("//li[contains(@class, '_ezgzd')]")
    # CommetClassList = driver.find_elements_by_xpath("//li[@class='gElp9']")
    CommetClassList = driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[2]/div[1]/ul")
    if len(CommetClassList) > 0:
        try:
            span = CommetClassList[0].find_element_by_css_selector('span')
            ContentList.append(span.text)
            ll = span.find_elements_by_css_selector('a')
            for l in ll:
                try:
                    hashTag = l.text
                    hashTagList.append(hashTag)
                        # print (hashTagLink)
                except:
                    continue
        except:
            print("exception1")

    with open(f'{save_name}.txt', '+a',encoding='utf-8') as f:
        # print ("one sample")
        writetime = '-'.join(writetime.split(' '))
        content = '\n'.join(ContentList)
        content = content.replace("\n", "/")
        content = content.replace("\t","_")
        content = content.replace(" ","_")
        hasLocation = hasLocation.replace(" ","_")
        hastTagStr = '_'.join(hashTagList)
        if content == "":
            content = "0"
            hastTagStr = "0"
        fea = writetime + '\t' + user + '\t' +  hasLocation + '\t' + content + '\t' + likeNum + '\t' + hastTagStr +'\n'
        print (fea)
        f.write(fea)


def f(driver,x):
    frame = []
    driver.get('https://www.instagram.com/p' + x)
    try:
        locationClass = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[2]/div[2]/a')
    except Exception as e:
        pass

    req = Request('https://www.instagram.com/p' + x, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml", from_encoding='utf-8')
    soup1 = soup.find("meta", attrs={"property": "og:description"})
    reallink1 = soup1['content']
    reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
    reallink1 = reallink1[:20]
    if reallink1 == '':
        return
    # mylist.append(reallink1)

    for reallink2 in soup.find_all("meta", attrs={"property": "instapp:hashtags"}):
        reallink2 = reallink2['content']
        reallink2 = reallink2[:10]
        mylist = []

        mylist.append(reallink1)
        mylist.append(reallink2)

        frame.append(mylist)

    print(str(num) + "개의 데이터 저장 중")
    num += 1
    data = pd.DataFrame(frame)
    data.to_csv('insta.txt', mode='+a', encoding='utf-8', header=None)

def login(driver):
    sleep(3)
    # 로그인 하기
    login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
    driver.find_element_by_xpath(login_section).click()
    sleep(2)

    elem_login = driver.find_element_by_name("username")
    elem_login.clear()
    # elem_login.send_keys('whatneed12')
    elem_login.send_keys('dohwanida')

    elem_login = driver.find_element_by_name('password')
    elem_login.clear()
    # elem_login.send_keys('fkdfldk1!')
    elem_login.send_keys('Ahtnsrks1')

    sleep(1)

    xpath = """//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button"""
    driver.find_element_by_xpath(xpath).click()

    sleep(4)

if __name__ == '__main__':
    freeze_support()
    print('### jinho021712@gmail.com ### Instacrawler Ver 0.1')

    print("pass")
    print("#크롤링 속도는 컴퓨터 사양에 따라 1.0 ~ 2.5 값으로 설정해주세요.")


    # scrolltime = float(input("크롤링 속도를 입력하세요 : "))
    scrolltime = 1.5
    # crawlnum = int(input("가져올 데이터의 수를 입력하세요 : "))
    # search = input("검색어를 입력하세요 : ")
    # savename = "서교동"
    savename = "여의도역"
    # savename = "양화로"

    driver = webdriver.Chrome(web_driver_path)
    search = urllib.parse.quote(savename)
    base_url = 'https://www.instagram.com/explore/tags/' + str(search) + '/'
    # base_url = 'https://www.instagram.com'
    driver.get(base_url)

    login(driver)

    # search_list = ["서교동", "양화로"]
    search_list = [savename]
    search_infos = {}
    sleep(5)
    search_window = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
    search_window.send_keys(savename)
    sleep(1.5)
    search_list = driver.find_element_by_xpath(
        "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div").find_elements_by_tag_name("a")
    sleep(1)
    for search in search_list:
        try:
            search_name, etc_info = search.text.split('\n')
        except Exception as e:
            search_name = search.text
            etc_info = "0"

        if "locations" in search.get_attribute("href"):
            search_infos[search_name] = [search.get_attribute("href"),etc_info]
        elif (search_name=="#서교동카페") or (search_name=="#서교동맛집") or (search_name=="#여의동"):
            search_infos[search_name] = [search.get_attribute("href"), etc_info]

    for idx,(search_name,search_info) in enumerate(search_infos.items()):
        reallink = defaultdict(list)
        if (idx==0) & (search_name=="서교동"):
            continue
        if (search_name == "서교동연습실roda") or(search_name=="서교동교회") or (search_name=="#서교동카페"):
            continue
        search_url, etc_info = search_info
        print(f'search_name : {search_name}\nsearch_url : {search_url}\netc_info : {etc_info}\n')
        driver.get(search_url)

        SCROLL_PAUSE_TIME = scrolltime
        num =0
        crawlnum = 600
        while num<crawlnum:
            pageString = driver.page_source
            bsObj = BeautifulSoup(pageString, "lxml")

            for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):
                row_post = link1.select('a')
                for post in row_post:
                    real = post.attrs['href']
                    reallink[search_name].append(real)

            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break

                else:
                    last_height = new_height
                    continue
            num+=1
        print(f"before set : {len(reallink[search_name])}")
        reallink[search_name] = list(set(reallink[search_name]))
        print(f"after set : {len(reallink[search_name])}")
        reallinknum = len(reallink[search_name])

        print(f"{search_name} : 총" + str(reallinknum) + "개의 데이터를 받아왔습니다.")
        for cnt,link in enumerate(reallink[search_name]):
            crawling(driver,link,savename)
        print("저장완료")
            # p = Pool(5)
            # p.map(f, reallink)
            # p.close()
            # p.join()
