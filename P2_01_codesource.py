
# -*- coding: utf-8 -*-

"""
The purpose of this program is to extract information from
the products on the Books to Scrap site.

"""
# Import needed package
import os
import requests

import pandas
from bs4 import BeautifulSoup


url_site = 'https://books.toscrape.com/index.html'

# Initialization of the category list
category_link_list = []

# Dictionary definition
data = {'Product_page_url': [],
        'Universal_Product_Code': [],
        'Title': [],
        'Price_including_tax': [],
        'Price_excluding_tax': [],
        'Number_avaible': [],
        'Product_description': [],
        'Category': [],
        'Review_rating': [],
        'Image_url': []}


def parse_url(url):
    """ This function parses the url passed as argument
    and returns the html page in text format
    format in order to extract the required elements.
    """

    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.text, 'html.parser')


def extract_product_info(url):
    """This function extracts the information from the products
    and loads them into the dictionary.
    """

    soup = parse_url(url)
    for link in soup.findAll('h3'):
        product_partial_link = link.find('a')['href'].split('..')[3]
        link_product = 'https://books.toscrape.com/catalogue'\
                       + product_partial_link
        soup = parse_url(link_product)
        product_page_url = link_product
        universal_product_code = soup.findAll('td')[0].text
        title = soup.find('h1').text
        price_incl_tax = soup.findAll('td')[2].text[2:]
        price_excl_tax = soup.findAll('td')[3].text[2:]
        number_avaible = soup.findAll('td')[5].text
        product_description = soup.findAll('p')[3].text
        category = soup.findAll('li')[2].text
        review_rating = soup.findAll('td')[6].text
        image_src = soup.find('img')['src'].split('..')[2]
        image_url = 'https://books.toscrape.com' + image_src

        data['Product_page_url'].append(product_page_url)
        data['Universal_Product_Code'].append(universal_product_code)
        data['Title'].append(title)
        data['Price_including_tax'].append(price_incl_tax)
        data['Price_excluding_tax'].append(price_excl_tax)
        data['Number_avaible'].append(number_avaible)
        data['Product_description'].append(product_description)
        data['Category'].append(category)
        data['Review_rating'].append(review_rating)
        data['Image_url'].append(image_url)


def export_data(info):
    """This function creates a folder to store the collected information
    in csv format as well as the images.
    """

    folder_name = data['Category'][0].split('\n')[1]
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    df = pandas.DataFrame(data, columns=[
        'Product_page_url', 'Universal_Product_Code',
        'Title', 'Price_including_tax', 'Price_excluding_tax',
        'Number_avaible', 'Product_description', 'Category',
        'Review_rating', 'Image_url'
        ])

    path = folder_name + '\\' + 'books.csv'
    if os.path.isfile(path):
        os.remove(path)
    df.to_csv(path, index=False)

    for i in range(len(data['Image_url'])):
        r = requests.get(data['Image_url'][i])
        with open(folder_name + '\\' + data['Universal_Product_Code'][i] + '.jpg', 'wb') as f:
            f.write(r.content)

    data['Product_page_url'] = []
    data['Universal_Product_Code'] = []
    data['Title'] = []
    data['Price_including_tax'] = []
    data['Price_excluding_tax'] = []
    data['Number_avaible'] = []
    data['Product_description'] = []
    data['Category'] = []
    data['Review_rating'] = []
    data['Image_url'] = []


def start(url):
    """This function extracts the url of the different categories
    and product pages.
    """

    print("Loading...")

    soup = parse_url(url_site)
    for i in range(1, 51):
        partial_link = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')[i]['href']
        category_link = url_site.split('index')[0] + partial_link
        category_link_list.append(category_link)

    for url_category in category_link_list:
        soup = parse_url(url_category)
        book_display = soup.find('form', {'class': 'form-horizontal'}).findAll('strong')

        if len(book_display) == 1:
            extract_product_info(url_category)
            export_data(data)
            print(str(category_link_list.index(url_category) + 1) + '/50')

        else:
            page_text = soup.find('li', {'class': 'current'}).text.strip()
            number_of_page = page_text.split(' ')[3]

            for i in range(1, int(number_of_page)+1):
                next_page_url = url_category.split('index')[0] + 'page-' + str(i) + '.html'
                soup = parse_url(next_page_url)
                page_text = soup.find('li', {'class': 'current'}).text.strip()
                current_page_number = page_text .split(' ')[1]

                if int(current_page_number) < int(number_of_page):
                    extract_product_info(next_page_url)
                else:
                    extract_product_info(next_page_url)
                    export_data(data)
                    print(str(category_link_list.index(url_category) + 1) + '/50')


start(url_site)
