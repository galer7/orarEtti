import csv
import re

# eu in range_orar am +1 celula in plus dupa grupele fiecarei serii.
# in grupe eu nu am asa ceva, deci trebuie tinut cont de asta.
# deci daca gasesc un curs/sem la indexul i, i se va atribui grupei i+

# exemplu output dorit:

# [{
#     'grupa': 'x',
#     'orar': {
#         'luni': { 
#             '9-11': {
#                 'type': 'sem/curs',
#                 'course': 'AM2',
#                 'room': 'A03'
#             }
#             ...
#         }
#         ...
#     }
#     'grupa': 'y',
#     ...
# ]

def findGroupIndex(event_index, length_serii):
    i = 0
    s = 0
    while(s + length_serii[i] < event_index):
        s = s + length_serii[i] + 1
        i = i + 1
    return event_index - i

orar = []

with open('orar_an1.csv') as f:
    reader = csv.reader(f)

    for row in reader:
        orar.append(row)

# taie chestiile useless
orar = orar[:70]

serii = list(filter(None, orar[0]))
pattern_serie = re.compile(r'Anul \w{1,3} Seria \w{1}')

# lista cu toate seriile si numarul de serii
serii = [x for x in serii if pattern_serie.findall(x)]
nr_serii = len(serii)

grupe = list(filter(None, orar[1]))
# print(grupe)
pattern_grupa = re.compile(r'4\d{2}\w{1,2}')

grupe = [x for x in grupe if pattern_grupa.findall(x)]
nr_grupe = len(grupe)

# trebuie sa stim cate grupe are fiecare serie (ajuta cu determinarea curs/sem):

length_serii = []
dict_serii = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

for letter in dict_serii:
    tmp_sum = 0
    for grupa in grupe:
        if(letter == grupa[3]):
            tmp_sum = tmp_sum + 1
    length_serii.append(tmp_sum)


effective_orar = nr_grupe + nr_serii
# print(effective_orar)

range_orar = [x[1:effective_orar+2] for x in orar[2:]] # inclusiv effective_orar
print(range_orar[0])

jump_cells = []
temps = 0
for ind, i in enumerate(length_serii):
    temps = temps + i
    jump_cells.append(temps)


for ind, i in enumerate(jump_cells):
    if(ind == 0):
        continue
    jump_cells[ind] = jump_cells[ind] + ind

range_zile = [x for x in range(3, len(orar), 13)]

for ind, i in enumerate(range_zile):
    if(ind == 0 or ind == 1):
        continue
    range_zile[ind] = range_zile[ind] + ind-1

range_zile.pop()
# print(range_zile)

zile = [[x, orar[x][0], ind] for ind, x in enumerate(range_zile)]
# print(zile)

iterator_zi = iter(zile)
zitmp = next(iterator_zi)

print(zitmp[1])
orar_final = [{} for x in grupe]

for grupa, orar_grupa in zip(grupe, orar_final):
    orar_grupa['grupa'] = grupa

# print(orar_final)

for ind_int, interval in enumerate(range_orar):
    if(ind_int > zitmp[0]):
        if zitmp[2] > 4:
            zitmp = next(iterator_zi)
            print(zitmp[1])
    for ind, cell in enumerate(interval[1:]):
        # ind_grupa = findGroupIndex(ind, length_serii)
        if cell == '' or ind in jump_cells:
            if cell != '':
                # print('___celula ignorata___:', cell)
                continue
        else:
            ind_grupa = findGroupIndex(ind, length_serii)
            for orar in orar_final:
                orar['orar'] = {}

            print(f'grupa {grupe[ind_grupa]} are {cell}')

print(orar_final)
# for thing in orar[2]