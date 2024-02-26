# api-web-scraping
Esta API destina-se a coletar os dados do cartão CNPJ de cada cnpj inserido em um arquivo input.csv
## Montar o app

1. Para executar o projeto é necessário clonar o repositório `git clone https://github.com/lacerdarenato/sysmap.git` dentro do diretório em deseja instalá-lo.
2. Instale as dependências contidas no arquivo requirements.txt através do comando `pip install -r requirements.txt`
3. Iniciar a aplicação executando o comando `python main.py` no diretório onde o projeto foi clonado
4. Crie um arquivo .env com as variáveis conforme o arquivo .env.example existente no projeto
5. Após a execução do programa serão criados 2 arquivos:
  - 1 com os dados coletados `collected_data.csv` 
  - 1 com os Cnpj's que falharam na busca `fail_list_cnpj.csv`