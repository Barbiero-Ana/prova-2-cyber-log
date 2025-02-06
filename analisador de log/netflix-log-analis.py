import csv
import json
from collections import Counter
from datetime import datetime

titulos = Counter()
perfis = Counter()
datas = Counter()

with open('All_ViewingActivity.csv', 'r') as arquivo:
    ler = csv.reader(arquivo)
    headers = next(ler)

    perfil_index = headers.index('Profile Name')
    comeco_index = headers.index('Start Time')
    titulo_index = headers.index('Title')

    for row in ler:
        if len(row) < max(perfil_index, comeco_index, titulo_index) + 1:
            continue

        perfil = row[perfil_index]
        comeco = row[comeco_index]
        titulo = row[titulo_index]

        titulos.update([titulo])
        perfis.update([perfil])
        date = comeco.split(' ')[0]
        datas.update([date])

# sessao de estilizacao pro dashboard - - - - - - - - - -

def cabecalho_print(titulo_cab):
    print(f"\n{'▶︎' * 50}")
    print(f"▾ {titulo_cab.upper():^44} ▾")
    print(f"{'▶︎' * 50}")

def data_format(date_for):
    try:
        data_obj = datetime.strptime(date_for, '%Y-%m-%d')
        return data_obj.strftime('%d-%m-%Y')
    except ValueError:
        return date_for

# sessao de estilizacao pro dashboard - - - - - - - - - -

# titulos
cabecalho_print('Conteúdo mais assistido')
print(f"{'Posição':<8} {'Título':<40} Visualizações")
print(f"{'-' * 60}")
for i, (titulo, count) in enumerate(titulos.most_common(10), 1):
    print(f"{f'{i}°':<8} {titulo[:37]:<40} {count:>6}")

# perfis

cabecalho_print('Atividade por perfil')
print(f"{'Perfil':<25} | {'Sessões':>10} | {'% do total':>10}")
print('-' * 50)
total = sum(perfis.values())
for perfil, count in perfis.most_common():
    percentual = (count / total) * 100
    print(f"{perfil[:22]:<25} | {count:>10,} | {percentual:>9.1f} %")

# Datas

cabecalho_print('Datas mais ativas')
print(f"{'Data':<12} | {'Dia da semana':<15} | Sessões")
print('-' * 40)
for date_for, count in datas.most_common(10):
    try:
        data_obj = datetime.strptime(date_for, '%Y-%m-%d')
        dia_semana = data_obj.strftime('%A')
        data_formatada = data_obj.strftime('%d-%m-%Y')
    except ValueError:
        dia_semana = 'Desconhecido'
        data_formatada = date_for
    print(f"{data_formatada:<12} | {dia_semana:<15} | {count}")

# all period

cabecalho_print('Período analisado')
data_sortida = sorted(datas.keys())
if data_sortida:
    prim = data_format(data_sortida[0])
    ult = data_format(data_sortida[-1])
    print(f"\n{'Primeira atividade:':<20} {prim}")
    print(f"{'Última atividade:':<20} {ult}")
else:
    print('Nenhuma atividade registrada...')

print(f"\n{'🀫' * 50}")
print(f"🀫🀫{'FIM DO RELATÓRIO':^46}🀫🀫")
print(f"\n{'🀫' * 50}")

# Agora, por ultimo... guardar tudo num bendito relatorio

data_sortida = sorted(datas.keys())
report = {
    'top_titulos': titulos.most_common(10),
    'atividade_perfil': dict(perfis),
    'data_atividade': datas.most_common(10),
    'primeira_atividade': data_sortida[0] if data_sortida else None,
    'ultima_atividade': data_sortida[-1] if data_sortida else None
}

with open('netflix_report.json', 'w') as arquivo:
    json.dump(report, arquivo, indent=4)
