import requests
from bs4 import BeautifulSoup 


with open("livre.text", "r") as inf:
	with open("Premier livre.csv", "w") as outf:
		outf.write("Product_page_url,Universal_Product_Code,Title,Price_including_tax,Price_excluding_tax,Product_description,Category,Review_rating, Image_url\n")

		urlPage = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

		r = requests.get(urlPage)

		if r.ok:
			soup = BeautifulSoup(r.text,"html.parser")
			product_page_url = urlPage
			universal_product_code = soup.findAll("td")[0].text
			title = soup.find("h1").text
			product_description = soup.findAll("p")[3].text
			price_including_tax = soup.findAll("td")[2].text
			price_excluding_tax = soup.findAll("td")[3].text
			category = soup.findAll('li')[2].text
			review_rating = soup.findAll("td")[6].text
			image_url = soup.find("img")["src"]
			outf.write(product_page_url + "," + universal_product_code +"," + title + "," + price_including_tax + "," + price_excluding_tax + "," + product_description + "," + category + "," + review_rating + "," + image_url + "\n")

			  
	



	







	