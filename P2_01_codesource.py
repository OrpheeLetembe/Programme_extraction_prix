import requests
from bs4 import BeautifulSoup 

urlPage = "http://books.toscrape.com/"

r = requests.get(urlPage)
print(r)