
# -*- coding: utf-8 -*-
"""
Programme d'extraction des informations produits de la catégorie travel du site books to scrape

"""

import requests
from bs4 import BeautifulSoup 
import csv

# Ouverture du fichier csv
csv_file = open("category.csv", "w",encoding="utf-8")
csv_writer = csv.writer(csv_file,delimiter=",",lineterminator="\n")

#Définition des entêtes de colonnes
csv_writer.writerow(["Product_page_url" , "Universal_Product_Code" , "Title" , "Price_including_tax" , "Price_excluding_tax" , "Number_avaible" , "Product_description" , "Category" , "Review_rating" , "Image_url"])

# Etractiontion de la page caterogie
url_category = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

reponse = requests.get(url_category)

if reponse.ok:
	liens = []
	soup = BeautifulSoup(reponse.text,"html.parser")
	places = soup.findAll("h3")
	for place in places:
		a = place.find("a")["href"].split("..")[3]
		lien = "https://books.toscrape.com/catalogue" + a

		r = requests.get(lien)

		if r.ok:
			soup = BeautifulSoup(r.text,"html.parser")
			product_page_url = lien
			universal_product_code = soup.find("table",{"class":"table table-striped"}).findAll("td")[0].text
			title = soup.find("div", {"class":"col-sm-6 product_main"}).h1.text
			price_including_tax = soup.find("table",{"class":"table table-striped"}).findAll("td")[2].text
			price_excluding_tax = soup.find("table",{"class":"table table-striped"}).findAll("td")[3].text
			number_avaible = soup.find("table",{"class":"table table-striped"}).findAll("td")[5].text
			product_description = soup.findAll("p")[3].text
			category = soup.find("ul",{"class":"breadcrumb"}).findAll("li")[2].text
			review_rating = soup.find("table",{"class":"table table-striped"}).findAll("td")[6].text
			image_src = soup.find("div",{"class":"item active"}).find("img")["src"].split("..")[2]
			image_url = "https://books.toscrape.com" + image_src

			#Ecriture des informations dans le fichier csv
			csv_writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_avaible, product_description, category, review_rating, image_url ])
					
		#fermeture du fichier csv
csv_file.close()
		
	






	






	