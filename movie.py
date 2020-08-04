from bs4 import BeautifulSoup
import requests
import csv

url = 'https://movie.naver.com/movie/running/current.nhn'
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

movie_list = soup.select(
    'div[id=content] > div.article > div.obj_section > div.lst_wrap > ul > li')

movie_code_list = []

for movie in movie_list:
    movie_dict={}
    a_tag = movie.select_one('dl > dt > a')
    title = a_tag.get_text()
    _ , code = a_tag['href'].split('code=')
    
    movie_dict = {
        'title': title,
        'code' : code
    }
    movie_code_list.append(movie_dict)
    
with open('movie_code.csv', 'w', newline='') as csvfile:
    fieldnames = ['title','code']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(movie_code_list)
print(movie_code_list)

