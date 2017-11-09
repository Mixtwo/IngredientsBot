import urllib.request
from bs4 import BeautifulSoup

class Product:

	def __init__(self, brand, name, img_url, product_url, ingredients):
		self.brand = brand
		self.name = name
		self.img_url = img_url
		self.product_url = product_url
		self.ingredients = ingredients

###################### search results page ################################

def get_first_search_result_soup(search_return_list):
	j = 0
	while j<len(search_return_list):
		soup_brand = search_return_list[j].find(attrs={'class': 'review-brand'}).text.strip()
		if soup_brand != "Beautypedia: Exclusives":
			return search_return_list[j]
		j+=1

def get_seach_results_page(queries):
	queries_str = queries.replace(' ', '+').lower()
	print(queries_str)

	search_url = "https://www.beautypedia.com/skin-care-reviews/?Ntt=" + queries_str
	html_search = urllib.request.urlopen(search_url)
	soup_search = BeautifulSoup(html_search, 'html.parser')
	search_return_list = soup_search.find_all('div', attrs={'class': 'review-col col-2'})
	
	#########
	zero_results = soup_search.find_all('div', attrs={'class': 'non-zero-results'})

	for false_results in zero_results:
		print("PRODUCT FOUND!")
		soup_single = get_first_search_result_soup(search_return_list)
		product_url = "https://www.beautypedia.com" + soup_single.find("a", href=True, attrs={'class': 'review-product'})['href']

		print(product_url)
		return product_url
	
	#########
	print("NO PRODUCT FOUND")
	return None

####################### product parsed page #################################

def get_soup_from_results_page(product_url):
	htmlfile = urllib.request.urlopen(product_url)
	soup = BeautifulSoup(htmlfile, 'html.parser')
	return soup

def product_info(soup, product_url):

	# brand name
	brand_box = soup.find(attrs={'class': 'brand-name'})
	brand = brand_box.text.strip()
	# print(brand)

	# product name
	product_box = soup.find(attrs={'class': 'product-name'})
	name = product_box.text.strip()
	# print(name)

	# product image link
	product_img_box = soup.find(attrs={'class': 'product-image'}).find("img")
	product_img = product_img_box["src"]
	# print(product_img)

	# ingredient list
	ingredients_box = soup.find(attrs={'class': 'content-item ingredients'})
	ingredients_text = ingredients_box.text.strip()
	ingredients = ingredients_text.split()
	# print(ingredients)

	product_details = Product(brand, name, product_img, product_url, ingredients)

	return product_details

######################### single methods for this class ##########################

def product_info_for(queries):
	product_url = get_seach_results_page(queries)

	if product_url == None:
		return None

	soup = get_soup_from_results_page(product_url)
	return product_info(soup, product_url)

######################## main ##############################################

