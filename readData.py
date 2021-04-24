import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import json
import numpy
import matplotlib.pyplot as plt
from collections import defaultdict
import math

# Passo a passo para instalar os pacotes necessários
# Pacotes para instalar
# pip3 install pandas
# pip3 install xlrd
# pip3 install matplotlib

# Colunas do excel
# Subject	FileName	AgeGroup	Age	Height	Mass	Gender	Dominance	LegLength	Static1	Static2	GaitSpeed(m/s)	TreadHands	FP_RightFoot	FP_LeftFoot	Notes	BorgScale


def convert(o):
    if isinstance(o, numpy.int64):
        return int(o)
    raise TypeError

# Capturar as idades
def getAges(data):
    age = set()
    return_age = []
    for d in data:
        if str(d['Age']) not in age:
            age.add(str(d['Age']))
            return_age.append(d['Age'])
        pass
    return return_age

# Capturando os voluntarios - sem repetição
def getVoluntarios(data):
    s = set()
    voluntarios = []
    for d in data:
        if str(d['Subject']) not in s:
            s.add(str(d['Subject']))
            voluntarios.append(d)
        pass
    return voluntarios


def lerArquivoExcel():
    arquivo = pd.read_excel("WBDSinfo.xlsx")
    return arquivo


def lerconverterDados(dados):
    array_data = []
    i = 0
    print("Lendo os dados da planilha...")
    for target_list in dados.index:
        array_data.append({
            "Subject": dados['Subject'][target_list],
            "FileName": dados['FileName'][target_list],
            "AgeGroup": dados['AgeGroup'][target_list],
            "Age": int(dados['Age'][target_list]),
            "Height": int(dados['Height'][target_list]),
            "Mass": int(dados['Mass'][target_list]),
            "Gender": dados['Gender'][target_list],
            "Dominance": dados['Dominance'][target_list],
            "LegLength": dados['LegLength'][target_list],
            "Static1": dados['Static1'][target_list],
            "Static2": dados['Static2'][target_list],
            "GaitSpeed(m/s)": dados['GaitSpeed(m/s)'][target_list],
            "TreadHands": dados['TreadHands'][target_list],
            "FP_RightFoot": dados['FP_RightFoot'][target_list],
            "FP_LeftFoot": dados['Notes'][target_list],
            "BorgScale": numpy.int64(dados['BorgScale'][target_list])
        })
        i = i + 1
        pass
    print("Total de dados lidos")
    print(i)
    listJson = json.dumps(array_data,  default=convert)
    dados_json = json.loads(listJson)
    return dados_json


def getMediaAlturaPorIdade(age, voluntarios):
    altura_array = []
    for x in age:
        count = 0
        altura = 0
        for i in voluntarios:
            if (i['Age'] == numpy.int(x)):
                altura = i['Height'] + altura
                count = count + 1
            pass
        media = altura / count
        altura_array.append(media)
        pass
    return altura_array

def getMediaGaitSpeedPorIdade(todosDados, voluntarios):
    array = []
    for voluntario in voluntarios:
        objeto = {}
        mediaGeitSpeed = 0
        count = 0
        for dado in todosDados:
            if (voluntario['Age'] == dado['Age']):
                if (dado['GaitSpeed(m/s)'] != '--' ):
                    mediaGeitSpeed = mediaGeitSpeed + dado['GaitSpeed(m/s)']
                    count = count + 1
            pass
        mediaGeitSpeed = mediaGeitSpeed / count
        objeto['mediaGaitSpeed'] = mediaGeitSpeed
        objeto['Age'] = voluntario['Age']
        array.append(objeto)
        pass
    pass
    return array    


def getMediaGaitSpeedPorVoluntario(voluntarios, todosDados):
    array = []
    for voluntario in voluntarios:
        objeto = {}
        mediaGeitSpeed = 0
        count = 0
        for dado in todosDados:
            if (voluntario['Subject'] == dado['Subject']):
                if (dado['GaitSpeed(m/s)'] != '--' ):
                    mediaGeitSpeed = mediaGeitSpeed + dado['GaitSpeed(m/s)']
                    count = count + 1
            pass
        mediaGeitSpeed = mediaGeitSpeed / count
        objeto['mediaGaitSpeed'] = mediaGeitSpeed
        objeto['subject'] = voluntario['Subject']
        array.append(objeto)
        pass
    pass
    return array

def mostrarGraficoIdadeAltura(age, altura):
    plt.bar(age, altura)
    plt.xlabel('Idade')
    plt.ylabel('Altura')
    plt.title('Média de altura por idade')
    plt.show()

def mostrarGraficoPorGender(dados):
    # fig1, ax1 = plt.subplots()
    size = [dados['qtd_masculino'], dados['qtd_feminino']]
    labels = 'Masculino' , 'Feminino'
    plt.pie(size, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
    plt.axis('equal') 
    plt.title('Quantidade de voluntarios por gênero')
    plt.show()
    pass

def mostrarGraficoPorGaitSpeedPorVoluntario(dados):
    subject = []
    mediaGaitSpeed = []
    for x in dados:
        subject.append(x['subject'])
        mediaGaitSpeed.append(x['mediaGaitSpeed'])
        pass
    pass
    plt.bar(subject, mediaGaitSpeed)
    plt.xlabel('subject')
    plt.ylabel('mediaGaitSpeed')
    plt.title('Média de GaitSpeed por Voluntarios')
    plt.show()

def mostrarGraficoPorGaitSpeedPorIdade(dados):
    subject = []
    mediaGaitSpeed = []
    for x in dados:
        subject.append(x['Age'])
        mediaGaitSpeed.append(x['mediaGaitSpeed'])
        pass
    pass
    plt.bar(subject, mediaGaitSpeed)
    plt.xlabel('Age')
    plt.ylabel('MediaGaitSpeed')
    plt.title('Média de GaitSpeed por Idade')
    plt.show()


def getQtdGender(data):
    objeto = {}
    groups = defaultdict(list)
    for obj in data:
        groups[obj['Gender']].append(obj) # agrupando por Subject
        pass
    qtd_masculino = sum(1 for x in data if x['Gender'] == 'M')
    qtd_feminino = sum(1 for x in data if x['Gender'] == 'F')
    objeto['qtd_Gender'] = groups.__len__()
    objeto['qtd_masculino'] = qtd_masculino
    objeto['qtd_feminino'] = qtd_feminino
    return objeto


if __name__ == "__main__":
    # Onde começa o programa chamando as funções
    todosDadosPlanilha = lerconverterDados(lerArquivoExcel())  # todos os dados da planilha
    dadosGender = getQtdGender(todosDadosPlanilha) # pegando qtd por genero
    voluntarios = getVoluntarios(todosDadosPlanilha)  # pegando os voluntarios
    age = getAges(todosDadosPlanilha)  # pegando as idades
    age = sorted(age)  # Ordenando as idades
    altura = getMediaAlturaPorIdade(age, voluntarios) # pegando a media de altura por idade
    dadosMediaGaitSpeedPorVoluntario = getMediaGaitSpeedPorVoluntario(voluntarios, todosDadosPlanilha)
    dadosMediaGaitSpeedPorIdade = getMediaGaitSpeedPorIdade(todosDadosPlanilha, voluntarios)



    mostrarGraficoIdadeAltura(age, altura)
    mostrarGraficoPorGender(dadosGender)
    mostrarGraficoPorGaitSpeedPorVoluntario(dadosMediaGaitSpeedPorVoluntario)
    mostrarGraficoPorGaitSpeedPorIdade(dadosMediaGaitSpeedPorIdade)

    
    pass

