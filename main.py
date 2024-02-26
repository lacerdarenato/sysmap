from playwright.sync_api import sync_playwright, expect
from solve_captcha import wait_seconds_to_user_click
from os import path, getcwd
import pandas as pd


def insert_cnpj(page, cnpj, ) -> bool:
    wait_seconds_to_user_click(3)
    page.locator("#cnpj").fill(cnpj)
    page.get_by_role("button", name="Consultar").click()
    
    if len(page.get_by_text("Aprovado pela Instrução Normativa RFB nº 2.119, de 06 de dezembro de 2022").all()) == 1:
        return True
    else:
        return False


def get_data_on_card(page):
    result = {}
    table = page.locator("#principal > table:nth-child(1) > tbody > tr > td > table").all()
    for lines in table:
        rows = lines.locator('tbody > tr > td ').all()
        
        for row in rows:
            fonts = row.locator('font').all()
            has_title = False
            if len(fonts) == 0:
                pass
            
            head = ''
            values = []
            
            for font in fonts:
                try:
                    if len(font.locator('b').all()) == 0 and not has_title:
                        head = font.inner_text(timeout=100)
                        has_title = True
                        
                    if len(font.locator('b').all()) == 1 and has_title:
                        values.append(font.locator('b').inner_text(timeout=100))
                    
                        if len(values) == (len(fonts) - 1):
                            result[head] = values
                    pass
                except:
                    pass
    # print(result)
    return result


def read_file(file_name):
    try:
        df = pd.read_csv(file_name)
        return df['CNPJs']
    except:
        return None


def get_columns()-> pd.DataFrame:
    return [
        'NOME EMPRESARIAL',
        'TÍTULO DO ESTABELECIMENTO (NOME DE FANTASIA)',
        'PORTE',
        'CÓDIGO E DESCRIÇÃO DA ATIVIDADE ECONÔMICA PRINCIPAL',
        'CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS',
        'CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA',
        'LOGRADOURO',
        'NÚMERO',
        'COMPLEMENTO',
        'CEP',
        'BAIRRO/DISTRITO',
        'MUNICÍPIO',
        'UF',
        'ENDEREÇO ELETRÔNICO',
        'TELEFONE',
        'ENTE FEDERATIVO RESPONSÁVEL (EFR)',
        'SITUAÇÃO CADASTRAL',
        'DATA DA SITUAÇÃO CADASTRAL',
        'MOTIVO DE SITUAÇÃO CADASTRAL',
        'SITUAÇÃO ESPECIAL',
        'DATA DA SITUAÇÃO ESPECIAL'
    ]


with sync_playwright() as p:
    #anchor
    cnpj_list = read_file('input.csv')
    
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    columns = get_columns()
    df = pd.DataFrame(columns=columns)
    fail_list_cnpj = []

    page.goto('https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp')
    try:
        for cnpj in cnpj_list:
            sucess = insert_cnpj(page, cnpj)
            if sucess:
                new_line = get_data_on_card(page)
                df = pd.concat([df, pd.DataFrame([new_line],  columns=columns)], ignore_index=True)
            else:
                fail_list_cnpj.append(cnpj)
            page.go_back()
    except:
        print('erro')
    finally:
        df.to_csv('collected_data.csv', index=False)
        pd.DataFrame(fail_list_cnpj).to_csv('fail_list_cnpj.csv', index=False)
    
    browser.close()