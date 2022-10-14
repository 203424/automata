import os
import string
from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA

NUM_ESTADOS = 30
estados = []
alfabeto_eng = []
simbolos = [chr(34),chr(39),chr(44),chr(32),chr(45),chr(95)] #{'"', "'", ',',' ','-', '_'}

for i in range(NUM_ESTADOS): #agrega tantos estados como se especifiquen en la variable NUM_ESTADOS
    state = 'q'+str(i)
    estados.append(state)
for c in string.ascii_letters:  #agrega las letras del alfabeto inglés mayusculas y minusculas
    alfabeto_eng.append(c)
for i in range(48,60): #agrega los simbolos con codigo ascii del 48 al 59 
    simbolos.append(chr(i)) #{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';'}

def crear_dict(lista,valor): #recibe una lista que usará como "clave" y un valor que se asignara a cada clave
    my_dict = dict()
    for c in lista:
        my_dict[c] = valor
    return my_dict #al final retorna un diccionario donde todas las claves tienen el mismo valor
#ej. {'a':'q14','b':'q14','c':'q14',...,'Z':'q14'}
dfa = DFA(
    states=set(estados),
    input_symbols=alfabeto_eng+simbolos,
    transitions={
        'q0': {'f': 'q1', ' ': 'q0','-':'q11'},
        'q1': {'o': 'q2'},
        'q2': {'n': 'q3'},
        'q3': {'t': 'q4'},
        'q4': {'-': 'q5'},
        'q5': {'f': 'q6'},
        'q6': {'a': 'q7'},
        'q7': {'m': 'q8'},
        'q8': {'i': 'q9'},
        'q9': {'l': 'q10'},
        'q10': {'y': 'q13'},
        'q11': {'-': 'q12'}, #el caracter ** sirve para unir dos diccionarios en un único diccionario
        'q12': dict({' ': 'q13',':':'q14','_':'q12','-':'q12'},**crear_dict(alfabeto_eng + simbolos[6:16],'q12')),
        'q13': {' ': 'q13',':':'q14'}, 
        'q14': dict({' ':'q14','"':'q15',"'":'q16'},**crear_dict(alfabeto_eng,'q17')), #simbolos[6:16] obtiene una nueva lista dado el rango de 6 al 16, este último no se incluye('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        'q15': crear_dict(alfabeto_eng,'q18'),
        'q16': crear_dict(alfabeto_eng,'q19'),
        'q17': dict({',':'q14',' ':'q20',';':'q21','-':'q22'},**crear_dict(alfabeto_eng + simbolos[6:16], 'q17')),
        'q18': dict({' ':'q23','"':'q27'},**crear_dict(alfabeto_eng + simbolos[6:16], 'q18')),
        'q19': dict({' ':'q24',"'":'q27'},**crear_dict(alfabeto_eng + simbolos[6:16], 'q19')),
        'q20': dict({' ':'q20',',':'q14',';':'q21'}, **crear_dict(alfabeto_eng + simbolos[6:16],'q25')),
        'q21': {},
        'q22': crear_dict(alfabeto_eng + simbolos[6:16],'q26'),
        'q23': crear_dict(alfabeto_eng + simbolos[6:16],'q18'),
        'q24': crear_dict(alfabeto_eng + simbolos[6:16],'q19'),
        'q25': dict({',':'q14',' ':'q20',';':'q21'},**crear_dict(alfabeto_eng + simbolos[6:16],'q25')),
        'q26': dict({',':'q14','-':'q22',';':'q21',' ':'q27'},**crear_dict(alfabeto_eng + simbolos[6:16],'q26')),
        'q27': {',':'q14',';':'q21',' ':'q27'},
        'q28': {',':'q14',';':'q29'},
        'q29': {},
    },
    initial_state='q0',
    final_states={'q17','q20','q21','q25','q26','q27','q28','q29'},
    allow_partial=True
)
#Se requiere instalar un programa de manera local para generar un archivo pdf con el automata
# dfa2 = VisualDFA(dfa)
# if os.path.exists("./dfa-extract-fonts.pdf") == False:
#     dfa2.show_diagram(filename='dfa-extract-fonts', format_type='pdf',path='./')

def leer_linea(archivo):
    lineas_validas = list()
    with open(archivo, 'r') as f:
        for line in f:
            if validar_linea(line.rstrip()) == True:
                lineas_validas.append(line.rstrip())
    return lineas_validas

def validar_linea(input_test):
    return dfa.accepts_input(input_test)