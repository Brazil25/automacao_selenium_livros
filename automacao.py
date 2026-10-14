from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)

df_produtos = pd.read_excel("Produtos.xlsx")

df_produtos["link"] = ""
df_produtos["preco"] = None

navegador = webdriver.Chrome()

WAIT = 10

def pesquisa_gutenberg(nome, autor, navegador):
    try:
        navegador.get("https://gutenberg.org/")

        busca = WebDriverWait(navegador, WAIT).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "search-input")
            )
        )

        busca.clear()
        busca.send_keys(str(nome))
        busca.send_keys(Keys.ENTER)

        WebDriverWait(navegador, WAIT).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "booklink")
            )
        )

        lista_resultados = navegador.find_elements(
            By.CLASS_NAME,
            "booklink"
        )

        lista_palavras_autor = str(autor).split()

        for resultado in lista_resultados:
            texto = resultado.text.lower()

            if str(nome).lower() in texto:

                if all(
                    palavra.lower() in texto
                    for palavra in lista_palavras_autor
                ):
                    link = resultado.find_element(
                        By.CLASS_NAME,
                        "link"
                    ).get_attribute("href")

                    return link, 0

    except Exception as erro:
        print(f"Erro Gutenberg ({nome}): {erro}")

    return None, None

for linha in df_produtos.index:

    nome = df_produtos.loc[linha, "nome"]
    autor = df_produtos.loc[linha, "autor"]
    categoria = df_produtos.loc[linha, "categoria"]

    print(f"Processando: {nome}")

    link, preco = pesquisa_gutenberg(
        nome,
        autor,
        navegador
    )

    df_produtos.loc[linha, "link"] = link
    df_produtos.loc[linha, "preco"] = preco


df_produtos.to_excel(
    "ProdutosAtualizado.xlsx",
    index=False
)

navegador.quit()

print("Concluído!")