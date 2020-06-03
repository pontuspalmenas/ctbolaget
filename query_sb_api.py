import requests
import sys
import json
import time

if len(sys.argv) != 2 or len(sys.argv[1]) < 1:
    print(f"Usage: {sys.argv[0]} [api-key]")
    sys.exit()

base_url = 'https://api-extern.systembolaget.se/product/v1/product/search?OriginLevel1=Champagne&SubCategory=Mousserande%20vin'
headers = {'Ocp-Apim-Subscription-Key':sys.argv[1]}

def get_json(url):   
    resp = requests.get(url, headers=headers, verify=False)
    if resp.status_code == 200:
        return json.loads(resp.text)
    if resp.status_code == 429:
        wait = int(resp.headers['Retry-After'])
        print(f"429 Too Many Requests. Waiting {wait} seconds...")
        time.sleep(wait)
    else:
        print(f"Request failed {resp.status_code} {resp.reason}")
        sys.exit()

bottles = []
def extract(hits):
    for h in hits:
        bottle = {}

        year = h['Vintage'] if h['Vintage'] > 0 else "NV"
        name = h['ProductNameBold']
        name2 = h['ProductNameThin']
        volume = h['Volume']
        bottle_type = h['BottleTextShort']
        if name2:
            name = f"{name} {name2}"

        # I'm just interested in standard and Magnum bottles for comparison
        # Note: need to check both packaging and size,
        # there are sets of two bottles in a case adding up to 1500 ml
        if bottle_type in ('Flaska', 'Magnum') and volume in (750.00, 1500.00):
            bottle['prodNr'] = h['ProductNumber']
            bottle['year'] = year
            bottle['name'] = name
            bottle['price'] = h['Price']
            bottles.append(bottle)

def write_file():
    with open('bolaget.json', 'w') as fp:
        json.dump(bottles, fp)

j = get_json(base_url)
extract(j['Hits'])

next_page = j['Metadata']['NextPage']
page_count = int((int(j['Metadata']['DocCount']) / len(j['Hits'])))
while next_page > 0:

    print(f"{next_page}/{page_count}")
    j = get_json(f"{base_url}&Page={next_page}")
    if j:
        extract(j['Hits'])
        next_page = j['Metadata']['NextPage']

write_file()
