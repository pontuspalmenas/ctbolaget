import re
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.cellartracker.com/list.asp?fInStock=0&Table=List&iUserOverride=0&Vintage=2010&Wine=Henri+Goutorbe+Champagne+Grand+Cru+Brut+Mill%E9sim%E9'
response = requests.get(base_url)
print(response.status_code)
soup = BeautifulSoup(response.text, parser="html.parser")
print(soup.find("div", {"id":"main_table"}))
