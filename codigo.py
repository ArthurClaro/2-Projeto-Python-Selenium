# criar um navegador
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import time 
import pandas as pd

# criar o navegador
nav = webdriver.Chrome()
# servico= Service(ChromeDriverManager().install())
# navegador = webdriver.Chrome(service=servico)


# importar/visualizar a base de dados
tabela_produtos = pd.read_excel("buscas.xlsx")
display(tabela_produtos)

def verifica_tem_termos_banidos(lista_termos_banidos, nome):
    tem_termos_banidos = False
    for palavra in lista_termos_banidos:
        if palavra in nome:
            tem_termos_banidos = True
    return tem_termos_banidos

def verifica_tem_todos_termos_produtos(lista_termos_nome_produto,nome):
    tem_todos_termos_produto = True
    for palavra in lista_termos_nome_produto:
        if palavra not in nome:
            tem_todos_termos_produto = False
    return tem_todos_termos_produto


def busca_google_shopping( nav , produto , termos_banidos, preco_minimo , preco_maximo):

    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(' ')
    lista_termos_nome_produto = produto.split(' ')
    lista_ofertas = []
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)

    #entar no google
    nav.get("https://www.google.com/")
    #digitar produto 
    nav.find_element( 'xpath', '//*[@id="APjFqb"]').send_keys(produto)
    nav.find_element( 'xpath', '//*[@id="APjFqb"]').send_keys(Keys.ENTER)

    #entrar na aba shopping 
    #percorrer a lista de elemento , se conter o texto shopping ele clica
    # nav.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()
    # esperar a pagina Do google renderizar 
    time.sleep(3)
    # OU
    # while len(nav.find_elements('class name', 'hdtb-mitem')) < 1:
    #     time.sleep(1)

    elementos = nav.find_elements('class name', 'hdtb-mitem')
    for item in elementos:
        if "Shopping" in item.text:
            item.click()
            break


    #pegar as inforaçoes do produto
    lista_resultados = nav.find_elements('class name','i0X6df')

    for resultado in lista_resultados:
        nome =  resultado.find_element( 'class name', 'tAxDx').text
        nome = nome.lower()

        #analisar se ele não tem nenhum termo banido (verificando se não é mini/watch)
        tem_termos_banidos = verifica_tem_termos_banidos(lista_termos_banidos,nome)

        
        #analisar se ele tem TODOS os termos do nome do produto(verificando se é 12/iphone/64gb)
        tem_todos_termos_produto = verifica_tem_todos_termos_produtos(lista_termos_nome_produto,nome)

        
        # seleciona só os elementos que tem tem_termos_banidos= False e ao mesmo tempo tem_todos_termos_produto = True
        # if tem_termos_banidos == False and tem_todos_termos_produto == True:
        # ou 
        if not tem_termos_banidos and tem_todos_termos_produto:

        #tratamento do preco(para verifica se esta no preco_minimo/maximo)
            preco =  resultado.find_element( 'class name', 'a8Pemb').text
            preco = preco.replace('R$','').replace(' ','').replace('.','').replace(',','.')
            preco = float(preco)

          
        # pegando o elemento pai pra poder pegar o Link .
            if preco_minimo <= preco <= preco_maximo:
                
                elemento_referencia = resultado.find_element('class name','bONr3b')
                elemento_pai = elemento_referencia.find_element('xpath','..') 
                link =  elemento_pai.get_attribute( 'href')
                # print(preco,nome,link) 
                lista_ofertas.append((nome,preco,link))
    return lista_ofertas     


def busca_buscape( nav , produto , termos_banidos, preco_minimo , preco_maximo):
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(' ')
    lista_termos_nome_produto = produto.split(' ')
    lista_ofertas = []
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)
    
    #entrando no site
    nav.get('https://www.buscape.com.br/')
    nav.find_element('xpath','//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div[2]/div/div[1]/input').send_keys(produto, Keys.ENTER)
   
    # time.sleep(3)
    #OUU posso fazer com time ou while 
    while len(nav.find_elements('class name', 'Select_Select__1S7HV')) < 1:
        time.sleep(1)

    # pegar os resultados
    lista_resultados = nav.find_elements('class name', 'SearchCard_ProductCard_Inner__7JhKb')

    for resultado in lista_resultados:
        preco = resultado.find_element('class name','Text_MobileHeadingS__Zxam2').text
        nome = resultado.find_element('class name','SearchCard_ProductCard_Name__ZaO5o').text
        nome = nome.lower()
        link = resultado.get_attribute('href')
        # print(nome,preco,link)

        #analisar se ele não tem nenhum termo banido (verificando se não é mini/watch)
        tem_termos_banidos = verifica_tem_termos_banidos(lista_termos_banidos,nome)
        
        #analisar se ele tem TODOS os termos do nome do produto(verificando se é 12/iphone/64gb)
        tem_todos_termos_produto = verifica_tem_todos_termos_produtos(lista_termos_nome_produto,nome)

        # analisa se o preço está entre o preço minimo e o preço maximo
        if not tem_termos_banidos and tem_todos_termos_produto:
            preco = preco.replace('R$','').replace(' ','').replace('.','').replace(',','.')
            preco = float(preco)
        
            if preco_minimo <= preco <= preco_maximo:
                lista_ofertas.append((nome,preco,link))
    
    return lista_ofertas     


tabela_ofertas = pd.DataFrame()

for linha in tabela_produtos.index:

    #pesquisa pelo produto
    produto = tabela_produtos.loc[linha,'Nome']
    termos_banidos = tabela_produtos.loc[linha,'Termos banidos']
    preco_minimo = tabela_produtos.loc[linha,'Preço mínimo']
    preco_maximo = tabela_produtos.loc[linha,'Preço máximo']

    lista_ofertas_google_shopping = busca_google_shopping( nav , produto, termos_banidos , preco_minimo , preco_maximo) 
    if lista_ofertas_google_shopping:
        tabela_google_shopping = pd.DataFrame(lista_ofertas_google_shopping, columns=['produto','preco','link'])
        # display(tabela_google_shopping)
        tabela_ofertas = pd.concat([tabela_ofertas,tabela_google_shopping])
    else:
        tabela_google_shopping = None
        
    lista_ofertas_buscape = busca_buscape( nav , produto, termos_banidos , preco_minimo , preco_maximo)
    if lista_ofertas_buscape:
        tabela_buscape = pd.DataFrame(lista_ofertas_buscape, columns=['produto','preco','link'])
        # display(tabela_buscape)
        tabela_ofertas = pd.concat([tabela_ofertas,tabela_buscape])
    else:
        tabela_buscape = None
    
display(tabela_ofertas)


#exportando para o Excel
tabela_ofertas.to_excel('Ofertas.xlsx', index=False)


#enviando e-mail
import win32com.client as win32 

if len(tabela_ofertas)>0:

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0) 
    mail.To = '0123456789arthur+compras@gmail.com'
    mail.Subject = 'Produto(s) Encontrado(s) na faixa de preço desejada'
    mail.HTMLBody = f"""
    <p>Prezados,</p>
    <p>Encontramos alguns produtos em oferta dentro da faixa de preço desejada. Segue tabela com detalhes</p>
    {tabela_ofertas.to_html(index=False)}
    <p>Qualquer dúvida estou à disposição</p>
    <p>Att.,</p>
    """
    
    mail.Send()

nav.quit()  