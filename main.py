import csv


def show_CSV(csv_file):
    for line in csv_file:
        line = line.split(',')
        print(line[14])

# csv_file = open('RID_DM_peso_familia_410750_WRAccAND_sim0.4k10ks2.csv', 'r')

# show_CSV(csv_file)


# def replace_at(string: str) -> str:
#     return string.replace("@", ",").replace("cod_", "")
#
# data_base = 'RID_DM_peso_familia_410750_WRAccAND_sim0.4k10ks2.csv'


# def modify_desc(csv_data):
#     for line in csv_data:
#         print(line[10].replace("@", ",").replace("cod_", ""))
#
#
#
# # Função para abrir arquivo CSV
# with open(data_base, 'r') as csv_file:
#         csv_reader = csv.reader(csv_file)
#
#         modify_desc(csv_reader)
        # show_CSV(csv_reader)


# for nome_coluna, valor_celula in zip(nomes_coluna, valores):
#     if nome_coluna == "desc":
#         print(replace_at(valor_celula))









