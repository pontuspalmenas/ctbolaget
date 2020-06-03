import requests
import sys
import json
import time

i = 0

if len(sys.argv) != 2 or len(sys.argv[1]) < 1:
	print(f"Usage: {sys.argv[0]} [api-key]")
	sys.exit()	

base_url = 'https://api-extern.systembolaget.se/product/v1/product/search?OriginLevel=Champagne&SubCategory=Mousserande%20vin'
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
	
def extract(hits):
	global i
	for h in hits:
		if h['OriginLevel1'] == 'Champagne':
			i = i + 1
			year = h['Vintage'] if h['Vintage'] > 0 else "NV"
			name = h['ProductNameBold']
			name2 = h['ProductNameThin']
			if name2:
				name = f"{name} {name2}"
			#print(f"{year} {name} {h['OriginLevel1']}")
	
j = get_json(base_url)
extract(j['Hits'])

next_page = j['Metadata']['NextPage']
while next_page > 0:
    print(f"{base_url}&Page={next_page}")
    j = get_json(f"{base_url}&Page={next_page}")
    if j:		
        extract(j['Hits'])
        next_page = j['Metadata']['NextPage']
	
print(i)