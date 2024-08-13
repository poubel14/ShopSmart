# ShopSmart

A ideia de criar esse código veio da falta de automação para definir qual supermercado teria os melhores preços de uma lista de compras ou de um produto específico.

Eu queria agilizar essa análise, e definir assim, qual local seria mais adequado para pedir minhas compras de supermercado baseado na lista de compras que eu fizesse.

Tomei como análise três supermercados que possuem e-commerce na minha região.

# Preparação Inicial

Utilizei as bibliotecas ‘BeautifulSoup’, ‘re’ e ‘request’ para a extração de dados, a biblioteca ‘time’ para definir tempos de execução da extração de dados, evitando a sobrecarga dos sites, a biblioteca ‘math’, para auxílio na busca pelo número de páginas de um dos sites, e a biblioteca ‘Pandas’, para tratamento dos dados para análise.

```
# Bibliotecas
import re
import math
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
```

Em seguida definimos as variáveis iniciais para extração e tratamento dos dados, e os padrões de busca para auxiliar na definição da quantidade de páginas após cada busca pelos produtos da lista de compras.

Esses dados foram sendo desenvolvidos ao longo do desenvolvimento do código.

```
# URL dos supermercados
CARONE_URL = 'https://www.carone.com.br/{item}?O=OrderByScoreASC#{page}'
EXTRAPLUS_URL = 'https://www.extraplus.com.br/busca/?q={item}&page={page}'
EXTRABOM_URL  = 'https://www.extrabom.com.br/busca/?q={item}&page={page}'

# Listas iniciais
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
```

Foi necessário utilizar uma opção para imitar um navegador de internet para aquisição de dados nos sites dos supermercados, pois eles tem uma restrição para uso direto de bots.

Isso me levou a utilizar tempos de atraso nas buscas para não comprometer o site, simulando uma busca de usuário.

É sempre válido analisar quais as restrições e limitações dos sites em relação a extração de dados, pois isso pode comprometer totalmente seu código. Sempre analise o robots.txt de cada site antes de pensar em extrair seus dados.

```
# Opções para imitar comportamento de um navegador de internet
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
           +'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
```

Os componentes utilizados em 'headers' para alimentar o servidor dos sites com infromações sobre o usuário que está utilizando o site são:

- "Mozilla/5.0": Ferramenta utilizada para identificação de navegadores e por questões de compatibilidade.
- "(Windows NT 10.0; Win64; x64)": Especificação do sistema operacional.
- "AppleWebKit/537.36": Indicação da ferramenta de renderização usada pelo navegador de internet. Esse é muito utilizado para navegadores como Safari e Chrome.
- "(KHTML, like Gecko)": Ferramenta para resolver problemas de compatibilidade com sistemas e programas antigos.
- "Chrome/114.0.0.0": Especificação do navegador de internet Chrome, na versão 114.0.0.0.
- "Safari/537.36": Especificação do navegador de internet Safari, mas também pode ser utilizado para resolver alguns problemas de compatibilidade.

Para dar entrada dos dados da lista de compras, fiz um input(), e separei as palavras digitadas antre virgulas, além de fazer com que tudo que fosse digitado ficasse em letras minúsculas.

```
# Pegar os dados da lista de compras do usuário
input_data = input("What do you want to buy?\n")
grocery_list = [item.strip() for item in input_data.lower().split(',')]
print('\nSearching...\n')
```

De início, comecei descobrindo como fazer a extração de dados do site de cada supermercado, entendendo as limitações de cada site para essa extração, e adaptando o código para cada caso.

```
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
```

```
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
```

```
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
```

Em um dos sites, foi possível perceber uma limitação de extração de dados apenas para a primeira página de busca por produtos, visto que não obtive sucesso com extração mesmo tentando utilizar métodos alternativos (selenium, playwright). A solução que tive para isso foi aproveitar os dados da primeira página mesmo, já que a primeira página já costuma vir os produtos mais relevantes ao item buscado.

```
# Execução das funções de busca dos itens da lista de compras
run_extraplus()
run_extrabom()
run_carone()
```

# Tratamento das informações extraídas dos sites

Ao finalizar a extração de dados dos sites, juntei os dados para inseri-los em um Dataframe, usando a biblioteca Pandas. Iniciando aqui a parte de análise das informações coletadas.

```
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
```

# Opções de análise

Após definir os códigos para extrair dados dos sites, decidi salvar os dados em arquivo .csv e .xlsx, para ter opções de análise. No caso do arquivo .xlsx, decidi não mexer nele pelo código, porque é possível ajustar pelo Programa Excel, deixei então como opção.

```
# Salva um arquivo csv
df.to_csv('C:\\Python\\project-one\\prices_grocery.csv', index=False)
# Salva um arquivo excel para analisar externamente (opcional)
df.to_excel('C:\\Python\\project-one\\prices_grocery.xlsx', index=False)

print("Search Completed."
      +"\nThe data has been saved to prices_grocery.xlsx and prices_grocery.csv files.")
```

Segui com o ajuste das informações pelo arquivo .csv, utilizando a biblioteca Pandas. Essa parte poderia ter sido feita em um modulo separado, mas decidi manter tudo junto para praticidade. Quero um código que apenas com a informação da Lista de Compras, já me forneca dados suficientes para eu saber qual mercado eu deveria fazer minhas compras.

Fiz um filtro para busca dos menores preços para cada produto na lista de compras e uma busca pelo supermercado que vale mais a pena ir para comprar essa lista de compras.

```
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
```

Decidi agrupar os dados para os melhores preços por produto, independente do supermercado. Essa informação já da uma noção de qual supermercado vale mais a pena pedir a lista de compras.

```
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
```

Em seguida agrupei dados para cada supermercado separadamente, com a descrição dos itens de melhor preço. Isso para analisar as maiores diferenças de preço e demonstrar a quantidade de produtos que cada supermercado tem disponível, dentre os produtos fornecidos pela Lista de Compras.

E para finalizar, forneci os dados de valores totais, caso faça a compra em cada um dos supermercados, ignorando quantidade de cada produto, pois não mudaria a decisão de qual mercado pedir minhas compras.

```
# Encontra os valores totais da lista de compras para cada supermercado
carone_total = sum(total_price[:(len(grocery_list))])
extrabom_total = sum(total_price[(len(grocery_list)):(2*(len(grocery_list)))])
extraplus_total = sum(total_price[(2*(len(grocery_list))):(3*(len(grocery_list)))])
print(f'Grocery List Total Value on Carone: R${carone_total:.2f}')
print(f'Grocery List Total Value on Extrabom: R${extrabom_total:.2f}')
print(f'Grocery List Total Value on Extraplus: R${extraplus_total:.2f}\n')
```

Dessa forma, o código me fornece os dados por produto e os dados de lista de compra por supermercado. Mostrando esses dados para tomada de decisão e também, armazenando essas informações para maiores análises, caso queiram.

# Possíveis ajustes futuros no Código

Ao longo da criação desse código, eu fiz algumas tentativas de tentar acelerar a aquisição de dados dos sites, mas esbarrei em limitações dos próprios sites, ou limitações de conhecimento em Web Scrape.

Possivelmente tenha algo que possibilite aquisição mais rápida, caso alguem tenha algo a acrescentar, adoraria saber.

Penso em fazer uma análise de histórico de preços, utilizando os arquivos .csv e/ou .xlsx, bem como análises de produtos com melhor preço por kg, tipo Manteiga de 200g ou Manteiga de 500g com um preço muito melhor. Ou preço do Pack de cerveja ou o valor da Lata ou Long neck separada.
