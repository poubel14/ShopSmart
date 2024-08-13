""" Project ShopSmart """

# Libraries
import re
import math
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Supermarket url's
CARONE_URL = 'https://www.carone.com.br/{item}?O=OrderByScoreASC#{page}'
EXTRAPLUS_URL = 'https://www.extraplus.com.br/busca/?q={item}&page={page}'
EXTRABOM_URL  = 'https://www.extrabom.com.br/busca/?q={item}&page={page}'

# Initial Lists
grocery_list = []
product_list_extraplus = []
price_list_extraplus = []
product_list_extrabom = []
price_list_extrabom = []
product_list_carone = []
price_list_carone = []
total_price = []

# Search patterns in the search for number of pages on website
EXTRAPLUS_PATTERN = r'page=(\d+)'
EXTRABOM_PATTERN = r'page=(\d+)'

# Option to mimic the behavior of a web browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
           +'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

# Get the user grocery list
input_data = input("What do you want to buy?\n")
grocery_list = [item.strip() for item in input_data.lower().split(',')]
print('\nSearching...\n')

# Working code for Extraplus Supermarket #

def run_extraplus():
    """ Search for products in grocery list on Extraplus Supermarket """
    for item in grocery_list:
        # Check how many pages of the searched item
        url = EXTRAPLUS_URL.format(item=item,page='1')
        res = requests.get(url, headers=headers, timeout=10)
        time.sleep(2)
        page_numbers = re.findall(EXTRAPLUS_PATTERN, res.text)
        try:
            num_pages = int(max(page_numbers))
        except Exception:
            num_pages = 1
            # Error handling when there is just one page on product search
        for page in range (1, num_pages+1):
            # Get the link of each page
            url = EXTRAPLUS_URL.format(item=item,page=page)
            res = requests.get(url, headers=headers, timeout=10)
            time.sleep(2)
            # Check for names and prices on this link
            if res.status_code == 200:
                bsoup = BeautifulSoup(res.content,'html.parser')
                product_names = bsoup.select(".name-produto p")
                product_prices = bsoup.select(".item-por__val")
                # Add names and prices to a list
                for name, price in zip(product_names, product_prices):
                    product_name = name.get_text(strip=True).lower()
                    product_price = price.get_text(strip=True)
                    try:
                        # Check if name and price exists
                        # Check if name is already in the list
                        if (product_name and product_price
                            and product_name not in product_list_extraplus):
                            # Search for each product specification
                            # Check if name start with the first word of product on grocery list
                            # Check if the next words are in the product description
                            for word in grocery_list:
                                word_parts = word.split()
                                if (product_name.startswith(word_parts[0])
                                    and all(subword in product_name for subword in word_parts[1:])):
                                    price_list_extraplus.append(product_price)
                                    product_list_extraplus.append(product_name)
                    except Exception:
                        pass # Error handling when not finding a product on this supermarket
            else:
                print(f"Failed to retrieve content: {res.status_code}")

# Working code for Extrabom Supermarket #

def run_extrabom():
    """ Search for products in grocery list on Extrabom Supermarket """
    for item in grocery_list:
        # Check how many pages of the searched item
        url = EXTRABOM_URL.format(item=item,page='1')
        res = requests.get(url, headers=headers, timeout=10)
        time.sleep(2)
        page_numbers = re.findall(EXTRABOM_PATTERN, res.text)
        try:
            num_pages = int(max(page_numbers))
        except Exception:
            num_pages = 1
            # Error handling when there is just one page on product search
        # Get the link of each page
        for page in range (1, num_pages+1):
            url = EXTRABOM_URL.format(item=item,page=page)
            res = requests.get(url, headers=headers, timeout=10)
            time.sleep(2)
            # Check for names and prices on this link
            if res.status_code == 200:
                bsoup = BeautifulSoup(res.content,'html.parser')
                product_names = bsoup.select(".name-produto")
                product_prices = bsoup.select(".item-por__val")
                # Add names and prices to a list
                for name, price in zip(product_names, product_prices):
                    product_name = name.get_text(strip=True).lower()
                    product_price = price.get_text(strip=True)
                    try:
                        # Check if name and price exists
                        # Check if name is already in the list
                        if (product_name and product_price
                            and product_name not in product_list_extrabom):
                            # Search for each product specification
                            # Check if name start with the first word of product on grocery list
                            # Check if the next words are in the product description
                            for word in grocery_list:
                                word_parts = word.split()
                                if (product_name.startswith(word_parts[0])
                                    and all(subword in product_name for subword in word_parts[1:])):
                                    if "$" in product_name and "," in product_name:
                                        product_name = product_name.replace(",", ".")
                                    price_list_extrabom.append(product_price)
                                    product_list_extrabom.append(product_name)
                    except Exception:
                        pass  # Error handling when not finding a product on this supermarket
            else:
                print(f"Failed to retrieve content: {res.status_code}")

# Working code for Carone Supermarket #

def run_carone():
    """ Search for products in grocery list on Carone Supermarket """
    for item in grocery_list:
        # Check how many pages of the searched item
        url = CARONE_URL.format(item=item,page='1')
        res = requests.get(url, headers=headers, timeout=10)
        time.sleep(2)
        items_found = BeautifulSoup(res.content, 'html.parser').find("span", class_="value")
        if items_found:
            num_pages = math.ceil(int(items_found.get_text(strip=True)) / 24)
        else:
            num_pages = 1
        # Get the link of each page
        for page in range (1, num_pages+1):
            url = CARONE_URL.format(item=item,page=page)
            res = requests.get(url, headers=headers, timeout=10)
            time.sleep(2)
            # Check for names and prices on this link
            if res.status_code == 200:
                bsoup = BeautifulSoup(res.content,'html.parser')
                product_names = bsoup.find_all(class_='product-name')
                product_prices = bsoup.find_all('addtocart-alternative-wc')
                # Add names and prices to a list
                for name, price in zip(product_names,product_prices):
                    product_name = name.get_text(strip=True).lower()
                    product_price = price.get('best-price','No best-price attribute found')
                    try:
                        # Check if name and price exists
                        # Check if name is already in the list
                        if (product_name and product_price
                            and product_name not in product_list_carone):
                            # Search for each product specification
                            # Check if name start with the first word of product on grocery list
                            # Check if the next words are in the product description
                            for word in grocery_list:
                                word_parts = word.split()
                                if (product_name.startswith(word_parts[0])
                                    and all(subword in product_name for subword in word_parts[1:])):
                                    price_list_carone.append(product_price)
                                    product_list_carone.append(product_name)
                    except Exception:
                        pass # Error handling when not finding a product on this supermarket
            else:
                print(f"Failed to retrieve content: {res.status_code}")

# Function's command to look for the grocery list
run_extraplus()
run_extrabom()
run_carone()

# Join all information for product name and price
products = product_list_carone + product_list_extrabom + product_list_extraplus
prices = price_list_carone + price_list_extrabom + price_list_extraplus
sources = (['Carone'] * len(product_list_carone) +
           ['Extrabom'] * len(product_list_extrabom) +
           ['Extraplus'] * len(product_list_extraplus))

# Set the table for the csv and xlsx files
df = pd.DataFrame({
    'Product': products,
    'Price': prices,
    'Supermarket': sources
})

# Save csv
df.to_csv('C:\\Python\\project-one\\prices_grocery.csv', index=False)
# Save excel to analyse externaly (optional)
df.to_excel('C:\\Python\\project-one\\prices_grocery.xlsx', index=False)

print("Search Completed."
      +"\nThe data has been saved to prices_grocery.xlsx and prices_grocery.csv files.")

# Organizing data from the csv file

# Load the CSV file
df = pd.read_csv('C:\\Python\\project-one\\prices_grocery.csv')

# Find the best price for each product and the corresponding supermarket
df['Price'] = df['Price'].replace({'R\\$': '', ',': '.', '\n': ' '}, regex=True).astype(float)
df['Product'] = df['Product'].replace({'\n': ' '}, regex=True)
print('\nBest Prices for each product:\n')
for product in grocery_list:
    try:
        f_data = df[df['Product'].str.contains(product.split()[0], case=False, na=False)]
        low_prices = f_data.loc[f_data['Price'].idxmin()]
        print(f'\t{low_prices.values[0]}: R${low_prices.values[1]} in {low_prices.values[2]}')
    except Exception:
        pass # Error handling when not finding a product on the grocery list
print('\n')

# Get the value of each item on grocery list for each supermarket
for brand in ['Carone','Extrabom','Extraplus']:
    b_df = df.loc[df["Supermarket"] == brand]
    print(f'Value of all grocery items on {brand}:\n')
    for product in grocery_list:
        try:
            f_df = b_df.loc[b_df['Product'].str.contains(product.split()[0], case=False, na=False)]
            low_prices = f_df.loc[f_df['Price'].idxmin()]
            print(f'\t{low_prices.values[0]}: R${low_prices.values[1]} in {low_prices.values[2]}')
            total_price.append(low_prices.values[1])
        except Exception as error_7:
            total_price.append(float(0.00))
            # Error handling when there is some items not found in the supermarket
    print('\n')

# Get the total value of the grocery list for each supermarket
carone_total = sum(total_price[:(len(grocery_list))])
extrabom_total = sum(total_price[(len(grocery_list)):(2*(len(grocery_list)))])
extraplus_total = sum(total_price[(2*(len(grocery_list))):(3*(len(grocery_list)))])
print(f'Grocery List Total Value on Carone: R${carone_total:.2f}')
print(f'Grocery List Total Value on Extrabom: R${extrabom_total:.2f}')
print(f'Grocery List Total Value on Extraplus: R${extraplus_total:.2f}\n')
