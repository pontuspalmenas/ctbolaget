import csv
import xml.etree.ElementTree as ET 

tree = ET.parse('sb_sortiment.xml')
root = tree.getroot()

print('year,name,name2,price,price_per_liter,size')
for i in root.findall("./artikel/[Ursprung='Champagne']"):
	
	year = i.find('Argang').text or "NV"
	name = i.find('Namn').text or ""
	name2 = i.find('Namn2').text
	if name2:
		name = f"{name} {name2}"
	packaging = i.find('Forpackning').text
	price = i.find('Prisinklmoms').text
	price_per_liter = i.find('PrisPerLiter').text
	size = i.find('Volymiml').text
	
	# I'm just interested in standard and Magnum bottles for comparison
	# Note: need to check both packaging and size, 
	# there are sets of two bottles in a case adding up to 1500 ml
	if packaging in ('Flaska', 'Magnum') and size in ('750.00', '1500.00'):
		print(f"{year},{name},{price},{price_per_liter},{size}")
