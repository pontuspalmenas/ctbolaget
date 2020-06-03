import requests
import sys
import json

base_url = 'https://bolaget.io/v1/products?origin=Champagne&product_group=Mousserande%20vin&limit=100'

def get(url):
    r = requests.get(url, verify=False)
    if r.status_code != 200:
        print(f"Request failed {r.status_code} {r.reason}")
        sys.exit()
    return r

def should_include(packaging, volume):
    # I'm just interested in standard and Magnum bottles for comparison
    # Note: need to check both packaging and size,
    # there are sets of two bottles in a case adding up to 1500 ml
    return packaging in ('Flaska', 'Magnum') and volume in (750, 1500)

bottles = []
def extract(hits):
    for h in hits:
        bottle = {}

        year = h['year'] or "NV"
        name = h['name']
        name2 = h['additional_name']
        volume = h['volume_in_milliliter']
        packaging = h['packaging']
        if name2:
            name = f"{name} {name2}"


        if should_include(packaging, volume):
            bottle['article_nr'] = h['article_nr']
            bottle['year'] = year
            bottle['name'] = name
            bottle['price_per_liter'] = h['price_per_liter']
            bottle['price'] = h['price']['amount']
            bottles.append(bottle)

def write_file():
    size = len(bottles)
    print(f"writing {size} bottles")
    with open('bolaget.json', 'w', encoding='utf-8') as fp:
        json.dump(bottles, fp, ensure_ascii=False)

resp = get(base_url)
jsn = json.loads(resp.text)

total_count = int(resp.headers['x-total-count'])
pages = total_count // 100 + (total_count % 100 > 0) # round up

extract(jsn)

offset = 0

for i in range(1, pages):
    offset = i * 100
    print(f"{i}/{pages}")
    resp = get(f"{base_url}&offset={offset}")
    jsn = json.loads(resp.text)
    extract(jsn)

write_file()
