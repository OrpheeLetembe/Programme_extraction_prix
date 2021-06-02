
# -*- coding: utf-8 -*-
"""
Programme d'extraction des informations produits du site books to scrape
"""

import requests
import pandas
#import csv
from bs4 import BeautifulSoup 



url_page = 'https://books.toscrape.com/index.html' 

# Création de la liste des liens des différentes catégories
category_link_list = []


#Création du dictionnaire de stockage des infos produit

data = {
		'Product_page_url':[],
		'Universal_Product_Code':[],
		'Title':[],
		'Price_including_tax':[],
		'Price_excluding_tax':[],
		'Number_avaible':[],
		'Product_description':[],
		'Category':[],
		'Review_rating':[],
		'Image_url':[]
		}


# fonction de création du csv 
def export_data(info):


	df = pandas.DataFrame(data, columns= ['Product_page_url' , 'Universal_Product_Code' , 'Title' , 
	'Price_including_tax' , 'Price_excluding_tax' , 'Number_avaible' , 
	'Product_description' , 'Category' , 'Review_rating' , 'Image_url'
	])

	file_name = category.split('\n')[1]

	#df.to_csv('data1.csv', index=False)
	df.to_csv(f'{file_name}.csv', index=False)  


	data['Product_page_url'] =[]
	data['Universal_Product_Code'] =[]
	data['Title'] =[]
	data['Price_including_tax'] =[]
	data['Price_excluding_tax'] =[]
	data['Number_avaible'] =[]
	data['Product_description'] =[]
	data['Category'] =[]
	data['Review_rating'] =[]
	data['Image_url'] =[]



#fonction d'extraction des informations produits
def extract_data(url):

	global category

	reponse = requests.get(url)

	if reponse.ok:
		soup = BeautifulSoup(reponse.text,'html.parser')
		links = soup.findAll('h3')

		for link in links:
			a = link.find('a')['href'].split('..')[3]
			link_product = 'https://books.toscrape.com/catalogue' + a
			r = requests.get(link_product)

			if r.ok:

				soup = BeautifulSoup(r.text,'html.parser')
				product_page_url = link_product
				universal_product_code = soup.find('table',{'class':'table table-striped'}).findAll('td')[0].text
				title = soup.find('div', {'class':'col-sm-6 product_main'}).h1.text
				price_including_tax = soup.find('table',{'class':'table table-striped'}).findAll('td')[2].text
				price_excluding_tax = soup.find('table',{'class':'table table-striped'}).findAll('td')[3].text
				number_avaible = soup.find('table',{'class':'table table-striped'}).findAll('td')[5].text
				product_description = soup.findAll('p')[3].text
				category = soup.find('ul',{'class':'breadcrumb'}).findAll('li')[2].text
				review_rating = soup.find('table',{'class':'table table-striped'}).findAll('td')[6].text
				image_src = soup.find('div',{'class':'item active'}).find('img')['src'].split('..')[2]
				image_url = 'https://books.toscrape.com' + image_src

							
				data['Product_page_url'].append(product_page_url)
				data['Universal_Product_Code'].append(universal_product_code)
				data['Title'].append(title)
				data['Price_including_tax'].append(price_including_tax)
				data['Price_excluding_tax'].append(price_excluding_tax)
				data['Number_avaible'].append(number_avaible)
				data['Product_description'].append(product_description)
				data['Category'].append(category)
				data['Review_rating'].append(review_rating)
				data['Image_url'].append(image_url)


#foncion de selection des pages des catégories
def parse_category_page(url):
	
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	a = soup.find('form', {'class':'form-horizontal'}).findAll('strong')

	if len(a) == 1:
		extract_data(url)
		export_data(data)

		#print(url)

		
	else:
		next_page_text = soup.find('li', {'class':'current'}).text.strip()
		next_page_number = next_page_text.split(' ')[3]
		#next_page_href = soup.find('li', {'class':'next'}).find('a')['href']

		for i in range (1, int(next_page_number)+1):
			next_page_url = url.split('index')[0] + 'page-' + str(i) + '.html'
			r = requests.get(next_page_url)
			soup = BeautifulSoup(r.text, 'html.parser')
			next_page_text = soup.find('li', {'class':'current'}).text.strip()
			page_num = next_page_text.split(' ')[1]
			
			if int(page_num) < int(next_page_number) : 
				extract_data(next_page_url)
				#print(next_page_url)
				#print(next_page_number)
				#print(page_num)	
			else:
				extract_data(next_page_url)
				export_data(data)
				#print(next_page_url)
				#print('export')	
				
						
				

#fonction d'extration des pages de catégorie
def parse_url_page(url):
	r = requests.get(url)
	if r.ok:
		soup = BeautifulSoup(r.text,'html.parser')
		for i in range (1, 51):
			url_category = soup.find('ul', {'class':'nav nav-list'}).findAll('a')[i]['href']
			category_link = url_page.split('index')[0]+ url_category
			category_link_list.append(category_link)

	for url in category_link_list:
		parse_category_page(url)


parse_url_page(url_page)	

