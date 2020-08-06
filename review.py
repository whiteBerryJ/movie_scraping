from bs4 import BeautifulSoup
import requests
import csv

url = 'https://movie.naver.com/movie/running/current.nhn'
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

# headers = {
#     'authority': 'movie.naver.com',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-dest': 'iframe',
#     'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
#     'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
#     'cookie': 'NNB=3WNJKKTQAMBV6; NRTK=ag#20s_gr#3_ma#-1_si#-1_en#-2_sp#-1; ASID=dc5f2a14000001736275a8740000004b; MM_NEW=1; NFS=2; MM_NOW_COACH=1; NMUPOPEN=Y; _ga=GA1.2.454277255.1596543073; BMR=s=1596675029864&r=https%3A%2F%2Fm.blog.naver.com%2Fsupapa13%2F221520270353&r2=https%3A%2F%2Fwww.google.com%2F; csrf_token=5782c249-9509-4491-be3e-91baf14809ed',
# }

# params = (
#     ('code', '189069'),
#     ('type', 'after'),
#     ('isActualPointWriteExecute', 'false'),
#     ('isMileageSubscriptionAlready', 'false'),
#     ('isMileageSubscriptionReject', 'false'),
# )

# response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=189069&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false', headers=headers)



movies_link = soup.select('div[id = content] > div.article > div:nth-child(1) > div.lst_wrap > ul > li')
hrefs=[]
titles=[]
for li in movies_link:
    href = li.select_one('dl > dt > a')['href']
    title = li.select_one('dl > dt > a').get_text()
    hrefs.append(href)
    titles.append(title)

movie_score_list = []
j=0
for link in hrefs:
    score_list = []
    score_list.append([titles[j]])
    print(titles[j])
    code = link.split('code=')[-1]

    headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': f'https://movie.naver.com/movie/bi/mi/point.nhn?code={code}',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=3WNJKKTQAMBV6; NRTK=ag#20s_gr#3_ma#-1_si#-1_en#-2_sp#-1; ASID=dc5f2a14000001736275a8740000004b; MM_NEW=1; NFS=2; MM_NOW_COACH=1; NMUPOPEN=Y; _ga=GA1.2.454277255.1596543073; BMR=s=1596675029864&r=https%3A%2F%2Fm.blog.naver.com%2Fsupapa13%2F221520270353&r2=https%3A%2F%2Fwww.google.com%2F; csrf_token=5782c249-9509-4491-be3e-91baf14809ed',
}
    params = (
        ('code', code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )
    req = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn',headers=headers, params=params)
    soup = BeautifulSoup(req.text, "html.parser")

    review_soup = soup.select_one('div.score_result')
    reviews = review_soup.select('li')

    

    for i, score in enumerate(reviews):

        star_score = score.select_one('div.star_score').text.strip()
        comment = score.select_one('#_filtered_ment_{}'.format(i))

        if score.select_one('span[id=_unfold_ment{}]'.format(i)):
            comment = comment.select_one('a')['data-src'].strip()
        else:
            comment = comment.get_text().strip()
        score_list.append([star_score, comment])
        if comment is None:
            continue
    
    movie_score_list.append(score_list)
    j+=1

with open('movie_score.csv', 'w', newline='') as csvfile:
    fieldnames = ['star_score','reple']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for row_pack in movie_score_list:
        writer.writerows(row_pack)

