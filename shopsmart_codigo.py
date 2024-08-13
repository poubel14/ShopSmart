""" Projeto ShopSmart """

# Bibliotecas
import re
import math
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL dos supermercados
CARONE_URL = 'https://www.carone.com.br/{item}?O=OrderByScoreASC#{page}'
EXTRAPLUS_URL = 'https://www.extraplus.com.br/busca/?q={item}&page={page}'
EXTRABOM_URL  = 'https://www.extrabom.com.br/busca/?q={item}&page={page}'

# Listas Iniciais
grocery_list = []
product_list_extraplus = []
price_list_extraplus = []
product_list_extrabom = []
price_list_extrabom = []
product_list_carone = []
price_list_carone = []
total_price = []

# Padrões de busca na procura pelo numero de paginas no site
EXTRAPLUS_PATTERN = r'page=(\d+)'
EXTRABOM_PATTERN = r'page=(\d+)'

# Opções para imitar comportamento de um navegador de internet
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
           +'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

# Pegar os dados da lista de compras do usuário
input_data = input("What do you want to buy?\n")
grocery_list = [item.strip() for item in input_data.lower().split(',')]
print('\nSearching...\n')

# Código para o Supermercado Extraplus #

def run_extraplus():
    """ Busca por produtos na lista de compras no Supermercado Extraplus """
    for item in grocery_list:
        # Definir quantas páginas tem no site após a busca de cada item da lista
        url = EXTRAPLUS_URL.format(item=item,page='1')
        res = requests.get(url, headers=headers, timeout=10)
        time.sleep(2)
        page_numbers = re.findall(EXTRAPLUS_PATTERN, res.text)
        try:
            num_pages = int(max(page_numbers))
        except Exception:
            num_pages = 1
            # Para lidar com o erro que ocorre quando tiver apenas uma página na busca por produto
        for page in range (1, num_pages+1):
            # Define o link para cada página
            url = EXTRAPLUS_URL.format(item=item,page=page)
            res = requests.get(url, headers=headers, timeout=10)
            time.sleep(2)
            # Pega os nomes e preços de cada link
            if res.status_code == 200:
                bsoup = BeautifulSoup(res.content,'html.parser')
                product_names = bsoup.select(".name-produto p")
                product_prices = bsoup.select(".item-por__val")
                # Adiciona nomes e preços na lista product_list_extraplus
                for name, price in zip(product_names, product_prices):
                    product_name = name.get_text(strip=True).lower()
                    product_price = price.get_text(strip=True)
                    try:
                        # Analisa se nomes e preços existem
                        # Analisa se nomes já estão na lista product_list_extraplus
                        if (product_name and product_price
                            and product_name not in product_list_extraplus):
                            # Busca especificações para cada produto
                            # Checando se o nome do produto no site começa com primeira palavra de um produto na lista de compra
                            # Checando se as palavras seguintes do item na lista de compras está na descrição do produto no site
                            for word in grocery_list:
                                word_parts = word.split()
                                if (product_name.startswith(word_parts[0])
                                    and all(subword in product_name for subword in word_parts[1:])):
                                    price_list_extraplus.append(product_price)
                                    product_list_extraplus.append(product_name)
                    except Exception:
                        pass # Para lidar com o erro que ocorre quando não encontrar um produto no site
            else:
                print(f"Failed to retrieve content: {res.status_code}")

# Código para o Supermercado Extrabom #

def run_extrabom():
    """ Busca por produtos na lista de compras no Supermercado Extrabom """
    for item in grocery_list:
        # Definir quantas páginas tem no site após a busca de cada item da lista
        url = EXTRABOM_URL.format(item=item,page='1')
        res = requests.get(url, headers=headers, timeout=10)
        time.sleep(2)
        page_numbers = re.findall(EXTRABOM_PATTERN, res.text)
        try:
            num_pages = int(max(page_numbers))
        except Exception:
            num_pages = 1
            # Para lidar com o erro que ocorre quando tiver apenas uma página na busca por produto
        for page in range (1, num_pages+1):
            # Define o link para cada página
            url = EXTRABOM_URL.format(item=item,page=page)
            res = requests.get(url, headers=headers, timeout=10)
            time.sleep(2)
            # Pega os nomes e preços de cada link
            if res.status_code == 200:
                bsoup = BeautifulSoup(res.content,'html.parser')
                product_names = bsoup.select(".name-produto")
                product_prices = bsoup.select(".item-por__val")
                # Adiciona nomes e preços na lista product_list_extrabom
                for name, price in zip(product_names, product_prices):
                    product_name = name.get_text(strip=True).lower()
                    product_price = price.get_text(strip=True)
                    try:
                        # Analisa se nomes e preços existem
                        # Analisa se nomes já estão na lista product_list_extrabom
                        if (product_name and product_price
                            and product_name not in product_list_extrabom):
                            # Busca especificações para cada produto
                            # Checando se o nome do produto no site começa com primeira palavra de um produto na lista de compra
                            # Checando se as palavras seguintes do item na lista de compras está na descrição do produto no site
                            for word in grocery_list:
                                word_parts = word.split()
                                if (product_name.startswith(word_parts[0])
                                    and all(subword in product_name for subword in word_parts[1:])):
                                    if "$" in product_name and "," in product_name:
                                        product_name = product_name.replace(",", ".")
                                    price_list_extrabom.append(product_price)
                                    product_list_extrabom.append(product_name)
                    except Exception:
                        pass  # Para lidar com o erro que ocorre quando não encontrar um produto no site
            else:
                print(f"Failed to retrieve content: {res.status_code}")

# Código para o Supermercado Carone #

def run_carone():
    """ Busca por produtos na lista de compras no Supermercado Carone """
    for item in grocery_list:
        # Definir quantas páginas tem no site após a busca de cada item da lista
        url = CARONE_URL.format(item=item,page='1')
        res = requests.get(url, headers=headers, timeout=10)
        time.sleep(2)
        items_found = BeautifulSoup(res.content, 'html.parser').find("span", class_="value")
        if items_found:
            num_pages = math.ceil(int(items_found.get_text(strip=True)) / 24)
        else:
            num_pages = 1
        # Define o link para cada página
        for page in range (1, num_pages+1):
            url = CARONE_URL.format(item=item,page=page)
            res = requests.get(url, headers=headers, timeout=10)
            time.sleep(2)
            # Pega os nomes e preços de cada link
            if res.status_code == 200:
                bsoup = BeautifulSoup(res.content,'html.parser')
                product_names = bsoup.find_all(class_='product-name')
                product_prices = bsoup.find_all('addtocart-alternative-wc')
                # Adiciona nomes e preços na lista product_list_carone
                for name, price in zip(product_names,product_prices):
                    product_name = name.get_text(strip=True).lower()
                    product_price = price.get('best-price','No best-price attribute found')
                    try:
                        # Analisa se nomes e preços existem
                        # Analisa se nomes já estão na lista product_list_carone
                        if (product_name and product_price
                            and product_name not in product_list_carone):
                            # Busca especificações para cada produto
                            # Checando se o nome do produto no site começa com primeira palavra de um produto na lista de compra
                            # Checando se as palavras seguintes do item na lista de compras está na descrição do produto no site
                            for word in grocery_list:
                                word_parts = word.split()
                                if (product_name.startswith(word_parts[0])
                                    and all(subword in product_name for subword in word_parts[1:])):
                                    price_list_carone.append(product_price)
                                    product_list_carone.append(product_name)
                    except Exception:
                        pass # Para lidar com o erro que ocorre quando não encontrar um produto no site
            else:
                print(f"Failed to retrieve content: {res.status_code}")

# Execução das funções de busca dos itens da lista de compras
run_extraplus()
run_extrabom()
run_carone()

# Junta toda informação de nomes e preços dos produtos dos supermercados
products = product_list_carone + product_list_extrabom + product_list_extraplus
prices = price_list_carone + price_list_extrabom + price_list_extraplus
sources = (['Carone'] * len(product_list_carone) +
           ['Extrabom'] * len(product_list_extrabom) +
           ['Extraplus'] * len(product_list_extraplus))

# Cria um dataframe para os arquivos csv e xlsx
df = pd.DataFrame({
    'Product': products,
    'Price': prices,
    'Supermarket': sources
})

# Salva um arquivo csv
df.to_csv('C:\\Python\\project-one\\prices_grocery.csv', index=False)
# Salva um arquivo excel para analisar externamente (opcional)
df.to_excel('C:\\Python\\project-one\\prices_grocery.xlsx', index=False)

print("Search Completed."
      +"\nThe data has been saved to prices_grocery.xlsx and prices_grocery.csv files.")

# Organizado os dados do arquivo .csv

# Carrega o arquivo CSV
df = pd.read_csv('C:\\Python\\project-one\\prices_grocery.csv')

# Encontra os melhores preços de cada produto e seu supermercado correspontente
df['Price'] = df['Price'].replace({'R\\$': '', ',': '.', '\n': ' '}, regex=True).astype(float)
df['Product'] = df['Product'].replace({'\n': ' '}, regex=True)
print('\nBest Prices for each product:\n')
for product in grocery_list:
    try:
        f_data = df[df['Product'].str.contains(product.split()[0], case=False, na=False)]
        low_prices = f_data.loc[f_data['Price'].idxmin()]
        print(f'\t{low_prices.values[0]}: R${low_prices.values[1]} in {low_prices.values[2]}')
    except Exception:
        pass # Para lidar com o erro que ocorre quando não encontrar um produto no site
print('\n')

# Encontra os valores de cada item da lista de compras para cada supermercado
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
            # Para lidar com o erro que ocorre quando não encontrar um produto no site
    print('\n')

# Encontra os valores totais da lista de compras para cada supermercado
carone_total = sum(total_price[:(len(grocery_list))])
extrabom_total = sum(total_price[(len(grocery_list)):(2*(len(grocery_list)))])
extraplus_total = sum(total_price[(2*(len(grocery_list))):(3*(len(grocery_list)))])
print(f'Grocery List Total Value on Carone: R${carone_total:.2f}')
print(f'Grocery List Total Value on Extrabom: R${extrabom_total:.2f}')
print(f'Grocery List Total Value on Extraplus: R${extraplus_total:.2f}\n')
