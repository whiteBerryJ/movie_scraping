from bs4 import BeautifulSoup
import requests


url = 'https://www.naver.com'
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

print(soup)

