# ShopSmart

The idea to make this project came when i realize that are no apps or programs, in my region, to help find out what supermarkets have the best prices for a grocery list or a specific product.

I wanted to make a quick analysis, and define where would be best to do grocery shopping.

I analysed the three supermarkets, in my region, that have e-commerce services.

### Getting things ready

I've used the libraries ‘BeautifulSoup’, ‘re’ e ‘request’ for web scraping; the library ‘time’, to set timers between commands, in order to avoid overloading the supermarket website servers; the library ‘math’, to help find for the number of pages after product search in one of the supermarket websites; and the library ‘Pandas’, to organize the data for further analysis.

```
# Libraries
import re
import math
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
```

Next we set the initial variables, for web scrape and data analysis, and the search patterns, to help discover the number of pages after product search on the websites.

These variables and patterns where defined along the development of the code.

```
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
```

It was necessary to use an option to mimic the web browser in order to web scrape on these websites, because of some restrictions related to direct use of bots.

These restrictions made me use the "time" library, to set timers before certain commands, and avoid overload the website server.

It is always valid to analyse the restrictions e limitations from websites you want to web scrape, because this can compromise your project. Check the robots.txt for each website, every time you want to extract data from them.

```
# Option to mimic the behavior of a web browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
           +'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
```

The components used in 'headers' to feed the server websites with information about the user accessing the website are:

- "Mozilla/5.0": That's a tool used to identify the browser and solve problems related to compatibility.
- "(Windows NT 10.0; Win64; x64)": Specify the Operational System.
- "AppleWebKit/537.36": Render engine tool used for the browser. Normally used for browsers like Safari and Chrome.
- "(KHTML, like Gecko)": Tool used to solve problems related to compatibility with older systems.
- "Chrome/114.0.0.0": Specify the browser Chrome, with the version 114.0.0.0.
- "Safari/537.36": Specify the browser Safari, and also used to solve problems related to compatibility.

To get input data, from the user, about the grocery shopping list, i've made a input(), split the words between commas, and lowercase everything, to help with the analysis.

```
# Get the user grocery list
input_data = input("What do you want to buy?\n")
grocery_list = [item.strip() for item in input_data.lower().split(',')]
print('\nSearching...\n')
```

In the begining, i've started learning how to scrape the data from each supermarket website, understanding it's limitations, and adapting the code for each website.

```
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
```

```
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
                            and product_name not in product_list_extraplus):
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
```

```
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
                            and product_name not in product_list_extraplus):
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
```

In one of the websites, i've noticed a restriction on web scrape, limiting the search only for the first page of the product search, due to some failed attempts i've had to extract the data on the other pages, even when i've tried to use other web scrape methods (Selenium, playwright). The solution was to get the data only from the first page, since the first page has the most relevant products anyway.

```
# Function's command to look for the grocery list
run_extraplus()
run_extrabom()
run_carone()
```

# Web Scrape data refining

After the conclusion of the web scrape. I've manage to join the data from all websites to create a Dataframe, using 'Pandas' library. From this point forward, it was all about data analysis.

```
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
```

# Options for Data analysis

After the conclusion and confirmation about the data extracted from the websites, i've decided to save the data on a .csv and .xlsx file, to have more options. For the .xlsx file, i've decided to refine the data outside the code, using Excel program, just as an option.

```
# Save csv
df.to_csv('C:\\Python\\project-one\\prices_grocery.csv', index=False)
# Save excel to analyse externaly (optional)
df.to_excel('C:\\Python\\project-one\\prices_grocery.xlsx', index=False)

print("Search Completed."
      +"\nThe data has been saved to prices_grocery.xlsx and prices_grocery.csv files.")
```

I've continued to organize the data in the .csv file, using 'Pandas' library. This part of the code could be writen in another module, but i've decided to keep all in one file because it was a relative small code already. I've wanted to make a code with only the grocery shopping list as input, and get just the necessary information (best supermarket prices and what supermarket has the best overall price).

I've made a filter to search for the lowest prices for each product, checking if the first word of the product match with the first word of the respective item on the grocery shopping list, also looking in the product description for the next information typed on the grocery list, and a search for the supermarket with the best price of the entire shopping list.

```
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
```

I've managed to group the data for best prices for each product. This information already give us the idea of the supermarket with the best prices.

```
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
```

Then, i've joined the data of prices for each supermarket, with product description. I've made this to help analysing the price fluctuation between supermarkets and to see how many products on the grocery shopping list were found in each supermarket.

And to finish the code, i've printed the total value of the grocery list, for each supermarket, ignoring the quantity of each product, as would be unecessary for our analysis.

```
# Get the total value of the grocery list for each supermarket
carone_total = sum(total_price[:(len(grocery_list))])
extrabom_total = sum(total_price[(len(grocery_list)):(2*(len(grocery_list)))])
extraplus_total = sum(total_price[(2*(len(grocery_list))):(3*(len(grocery_list)))])
print(f'Grocery List Total Value on Carone: R${carone_total:.2f}')
print(f'Grocery List Total Value on Extrabom: R${extrabom_total:.2f}')
print(f'Grocery List Total Value on Extraplus: R${extraplus_total:.2f}\n')
```

In the end, the code print the data for product and the data for grocery shopping list for each supermarket. Showing these data to decide where to buy and also, storing this information for further analysis, as an option.

# Future ajustments in the code

Upon the development of this code, i've made attempts to make the search faster on data extraction from the websites, but got some dificulties with restrictions from these websites, or maybe i need more study on web scrape.

Maybe is possible to make it faster. If anyone have any ideas, i would love to know.

I'm thinking on doing analysis for history prices, using the .csv and .xlsx files saved, and also analysis about products with best prices by weight, like butter of 200g or butter of 500g with a much better price, or the price of one beer versus the price of one beer on a pack.
