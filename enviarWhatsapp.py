# usado para controle dos arquivos
import pandas as pd

# usado para fazer pausas no programa
import time

# usado para controlar o navegador
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib

contatos_df = pd.read_excel("ContatosEnviar.xlsx")
print(contatos_df)

time.sleep(3)

# carregamento do whatsapp web
navegador = webdriver.Chrome()
navegador.get("https://web.whatsapp.com/")

# espera aparecer o elemento que tem id de "side"
while len(navegador.find_elements(By.ID ,"side")) < 1 :
    time.sleep(1)

print("Login feito")


# pego todos os dados na tabela com o for
for i, numero in enumerate(contatos_df['NÚMERO']):
    # mensagem = contatos_df.loc[i, "Mensagem"]
    # caso queira outra mensagem ou uma mensagem unica para todos 
    # os usuários descomente a linha abaixo e insira sua mensagem:
    mensagem ="""Olá, essa mensagem é automática.
Todos os usuários da lista deveram receber o mesmo texto.""" 
    pessoa = contatos_df.loc[i, "PESSOA"].split()[0]
    numeroToSend = f"5511{numero}"
    # defino qual sera o texto e converto para url encode
    texto = urllib.parse.quote(f"Oi {pessoa}, tudo bom com você?\n{mensagem}")
    #crio o link de navegação
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    # vou até o link de envio
    navegador.get(link)

    # espera aparecer o elemento que tem id de "side"
    while len(navegador.find_elements(By.ID ,"side")) < 1 :
        time.sleep(1)

    time.sleep(7)
    # xpath do campo que tem que apertar enter
    # //*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p
    navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p').send_keys(Keys.ENTER)
    time.sleep(5)