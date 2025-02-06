import csv
import json
from collections import Counter
from datetime import datetime


metodos = Counter()
ips = Counter()
status = Counter()
error = 0 #contator pros erros

with open ('weblog.csv', 'r') as arquivo:
    ler = csv.reader(arquivo)
    next(ler) #pula o titulo/ cabecalho
    for row in ler:
        if len(row) < 4:
            continue # aqui eu to ignorando linhas mal formatadas
        ip, date, metodo_url, status_log = row
        metodo = metodo_url.split(' ')[0]
        metodos.update([metodo])
        ips.update([ip])
        status.update([status_log])
        if status_log.startswith('4') or status_log.startswith('5'):
            error += 1

# sessao de estilizacao pro dashboard - - - - - - - - - -

def cabecalho_print(titulo):
    print(f'\n{'=' * 50}') # cria a sequencia de '='na hora do print pra ficar bonitinho
    print(f'|| {titulo.upper():^44} ||')
    print(f'{'=' * 50}')

def tabelas(colunas, counter):
    print(f'\n{colunas[0]:<20} | {colunas[1]:>15}')
    print('-' * 38)
    for item, count in counter.most_common():
        print(f'{item:<20} | {count:>15}')

#relatorio no terminallll
print(f'\n{'*' * 50}')
print(f'** {'ANÁLISE DE LOG - RELATÓRIO':^46} **')
print(f'{'Gerado em':<20} {datetime.now().strftime('%d/%m/%Y %H:%M')}') #formatacao da hora em tempo real
print(f'{'*' * 50}')

#HTTP
cabecalho_print('métodos HTTP')
tabelas(['Método', 'Requisições'], metodos)

# IPS
cabecalho_print('Ips mais ativos')
print(f'{'Posição':<10} {'IP':<20} Acessos')
print(f'{'-' * 40}')
for i, (ip, count) in enumerate(ips.most_common(5), 1):
    print(f'{i:<10} {ip:<20} {count:,}')

#eeross
cabecalho_print('Erros detectados')
print(f'\n{' TOTAL DE ERROS: ':^50}')
print(f'{" ":10} {error:^30,} {" ":10}')
print(f'{'*' * 50}')

#sastus coded
cabecalho_print('Distribuição de status')
tabelas(['Status code', 'Ocorrências'], status)

print(f'\n{"*" * 50}')
print(f'**{"FIM DO RELATÓRIO":^46}**')
print(f'{"*" * 50}')

# agora salvar o relatório em algum canto n é mesmoooooo

report = {
    'metodo_http': dict(metodos), #o dict permite associar uma chave única a um valor especifico
    'top_ips': ips.most_common(5),
    'errors': error,
    'status_distribuicao': dict(status)
}

with open('weblog_report.json', 'w') as arquivo:
    json.dump(report, arquivo, indent=4)
