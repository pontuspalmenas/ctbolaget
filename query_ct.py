import re
import requests
from bs4 import BeautifulSoup

# open bolaget.json
# for each entry
# query cellartracker and parse score
# add score to object
# save as ctbolaget.json


#base_url = 'https://www.cellartracker.com/list.asp?fInStock=0&Table=List&iUserOverride=0&Vintage=2010&Wine=Henri+Goutorbe+Champagne+Grand+Cru+Brut+Mill%E9sim%E9'
#response = requests.get(base_url)
#print(response.status_code)

with open("ct.html", "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')        

#soup = BeautifulSoup(response.text, parser="html.parser")
    score_span = soup.find("span", {"class":"scr"})
    print(score_span.a.text.split(" ", 1)[0])

