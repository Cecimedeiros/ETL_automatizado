import pandas as pd
import os
import urllib.parse
import requests

PANDAS_READ_FUNCTIONS = {
    '.csv': pd.read_csv,
    '.json': pd.read_json,
    '.xlsx': pd.read_excel,
    '.xls': pd.read_excel
}

def extraction(url: str):
    parsed_url = urllib.parse.urlparse(url) 
    file_path = parsed_url.path 
    splitresult= os.path.splitext(file_path)
    file_extension= splitresult[1]
    file_extension= file_extension.lower()

    data = None
    
    if file_extension in PANDAS_READ_FUNCTIONS:
        try:
            read = PANDAS_READ_FUNCTIONS.get(file_extension)
            data = read(url)
            print(f"Dados extraídos com sucesso do arquivo {file_extension.upper().replace('.', '')}!")
        except Exception as e:
            print(f"Erro ao tentar extrair dados do arquivo {file_extension.upper()} devido a {e}")
            data = None

    elif url.startswith('https://'):
        try:
            response= requests.get(url)
            response.raise_for_status()

            data = pd.DataFrame(response.json())
            print(f"Dados extraidos com sucesso da API {url}")

        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição ao acessar a API '{url}': {e}")
            data = None

    else:
        print("Tipo de dado desconhecido!")

    return data
    
    
def main():
    url = "C:/Users/souza/Downloads/Sleep_health_and_lifestyle_dataset.csv"
    extracted_data = extraction(url)
    if extracted_data is not None:
        print("\nPrimeiras 5 linhas dos dados extraidos:")
        print(extracted_data.head(10))

if __name__ == "__main__":
    main()
    