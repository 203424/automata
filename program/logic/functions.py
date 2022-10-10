import os
import string
from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA

NUM_ESTADOS = 31

estados = []
alfabeto_eng = []
simbolos = [chr(34),chr(39),chr(44),chr(32),chr(45),chr(95)] #{'"', "'", ',',' ','-', '_'}

for i in range(NUM_ESTADOS): #agrega tantos estados como se especifiquen en la variable NUM_ESTADOS
    state = 'q'+str(i)
    estados.append(state)
for c in string.ascii_lowercase:  #agrega las letras minusculas del alfabeto inglés
    alfabeto_eng.append(c)
for c in string.ascii_uppercase: #agrega las letras mayusculas del alfabeto inglés
    alfabeto_eng.append(c)
for i in range(48,60): #agrega los simbolos con codigo ascii del 48 al 59 
    simbolos.append(chr(i)) #{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';'}

def crear_dict(lista,valor): #recibe una lista que usará como "clave" y un valor que se asignara a cada clave
    my_dict = dict()
    for c in lista:
        my_dict[c] = valor
    return my_dict #al final retorna un diccionario donde todas las claves tienen el mismo valor
#ej. {'a':'q15','b':'q15','c':'q15',...,'Z':'q15'}
dfa = DFA(
    states=set(estados),
    input_symbols=alfabeto_eng+simbolos,
    transitions={
        'q0': {'f': 'q1', ' ': 'q12','-':'q13'},
        'q1': {'o': 'q2'},
        'q2': {'n': 'q3'},
        'q3': {'t': 'q4'},
        'q4': {'-': 'q5'},
        'q5': {'f': 'q6'},
        'q6': {'a': 'q7'},
        'q7': {'m': 'q8'},
        'q8': {'i': 'q9'},
        'q9': {'l': 'q10'},
        'q10': {'y': 'q11'},
        'q11': {':': 'q16', ' ': 'q11'},
        'q12': {' ': 'q12', '-': 'q13','f':'q1'},
        'q13': {'-': 'q14'}, #el caracter ** sirve para unir dos diccionarios en un único diccionario
        'q14': dict({'-':'q15','_':'q15'},**crear_dict(alfabeto_eng + simbolos[6:16],'q15')), #simbolos[6:16] obtiene una nueva lista dado el rango de 6 al 16, este último no se incluye('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        'q15': dict({'-':'q15','_':'q15',':':'q16', ' ': 'q11'}, **crear_dict(alfabeto_eng + simbolos[6:16],'q15')),
        'q16': dict({'"':'q17',"'":'q17','-':'q19',' ':'q16'}, **crear_dict(alfabeto_eng,'q18')),
        'q17': crear_dict(alfabeto_eng,'q20'),
        'q18': dict({',':'q16',' ':'q22','-':'q22',';':'q21'},**crear_dict(alfabeto_eng + simbolos[6:16], 'q18')),
        'q19': crear_dict(alfabeto_eng,'q23'),
        'q20': dict({'"':'q24',"'":'q24',' ':'q25'}, **crear_dict(alfabeto_eng + simbolos[6:16],'q20')),
        'q21': {},
        'q22': dict({' ':'q22',',':'q16',';':'q21'},**crear_dict(alfabeto_eng + simbolos[6:16],'q26')),
        'q23': dict({'-':'q27'}, **crear_dict(alfabeto_eng + simbolos[6:16],'q23')),
        'q24': {';':'q28',',':'q16'},
        'q25': crear_dict(alfabeto_eng + simbolos[6:16],'q20'),
        'q26': dict({',':'q16',' ':'q22','-':'q22',';':'q21'},**crear_dict(alfabeto_eng + simbolos[6:16],'q26')),
        'q27': crear_dict(alfabeto_eng,'q29'),
        'q28': {},
        'q29': dict({';':'q21',' ':'q30',',':'q16'},**crear_dict(alfabeto_eng + simbolos[6:16],'q29')),
        'q30': {' ':'q30',',':'q16',';':'q21'}
    },
    initial_state='q0',
    final_states={'q18','q21','q22','q24','q26','q27','q28','q29','q30'},
    allow_partial=True
)

dfa2 = VisualDFA(dfa)
if os.path.exists("./dfa-extract-fonts.pdf") == False:
    dfa2.show_diagram(filename='dfa-extract-fonts', format_type='pdf',path='./')

def obtener_transiciones():
    filas = list()
    for i in range (0,31):
        filas.append(dfa2.table.iloc[i])
    for fila in filas:
        for x in fila:
            print(str(x)+" ", end="")
        print("\n")
    # print(dfa2.table)

def leer_linea(archivo):
    lineas_validas = list()
    with open(archivo, 'r') as f:
        for line in f:
            if validar_linea(line.rstrip()) == True:
                lineas_validas.append(line.rstrip())
    return lineas_validas

def validar_linea(input_test):
    return dfa.accepts_input(input_test)