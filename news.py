from bs4 import BeautifulSoup
import requests
import csv
soup_objects = []
for i in range(1, 102, 10):
    base_url = 'https://search.naver.com/search.naver?&where=news&query=광주인공지능사관학교&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=47&start='
    start_num = i
    end_url = '&refresh_start=0'

    URL = base_url + str(start_num) + end_url

    req = requests.get(URL)
    soup = BeautifulSoup(req.text, "html.parser")

    soup_objects.append(soup)


for soup in soup_objects:
    text = soup.select(
        'div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul > li' )

    news_data = {
        'title' : '',
        'link' : ''
    }


    for a in text:
        atag = a.select_one('dl > dt > a')
        # print(atag_list)
        
        news_data['title'] = atag['title']
        news_data['link'] = atag['href']
        print(atag['title'], atag['href'])

        # append 모드이므로 같은 파일에 계속 추가되지는 않는 지 확인해보기
        # utf-8 인코딩을 쓰면 한글이 깨진다. 왜그러지?
        with open('new3.csv', 'a', newline='') as csvfile:
            fieldnames = ['title','link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'title':atag['title'], 'link':atag['href']})
