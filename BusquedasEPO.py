from bs4 import BeautifulSoup
import epo_ops

# Insrtar Keys cuenta EPO ( www.epo.org )
consumer_key = ''
consumer_secret_key = ''


def initEPO(consumer_key=consumer_key,
            consumer_secret_key=consumer_secret_key):
    return epo_ops.Client(key=consumer_key, secret=consumer_secret_key)


def busquedaEPO(response, elemento='abstract', type='html'):
    fin = []
    if type == 'html':
        soup = getSoup(response, 'html.parser')
        aux = soup.find_all(elemento)
        for i in aux:
            fin.append(i.string)
    elif type == 'xml':
        soup = getSoup(response, 'xml')
        aux = soup.find_all(elemento)
        for i in aux:
            fin.append(i.p.string)
    return fin


def busquedaLang(response, idioma='en', type='xml'):
    #fin = list()
    soup = getSoup(response, type)
    aux = soup.find(lang=idioma)
    if aux != None:
        return aux.p.string
    else:
        return None


def publicNumber(country, number):
    return [str(country[i]) + str(number[i]) for i in range(len(country))]


def getSoup(response, type='html.parser'):
    return BeautifulSoup(response.text, type)


def allEPO(where="ta", list=[]):
    ##Criterio de busqueda, todos los documentos que contengas todas las palabras de list en where
    ## ej. where="ta" list=["green", "energy"] busca todos los documentos que contengas green energy en sus titulos o abstract.
    aux = where + ' all  "'
    for i in range(len(list)):
        if i == 0:
            aux += list[i]
        elif i >= 5:
            aux += ', ' + list[i]
            break
        else:
            aux += ', ' + list[i]
    return aux + '"'


def anyEPO(where="ta", list=[]):
    #Criterio de busqueda, todos los documentos que contengas alguna de las palabras de list en where
    ## ej. where="ta" list=["green", "energy"] busca todos los documentos que contengas green o energy en sus titulos o abstract.
    ## maximo de 5 palabras.
    aux = where + ' any  "'
    for i in range(len(list)):
        if i == 0:
            aux += list[i]
        elif i >= 5:
            aux += ', ' + list[i]
            break
        else:
            aux += ', ' + list[i]
    return aux + '"'


def dataEPO(where="pd", data1="20150101", data2="20170101"):
    #Criterio de busqueda, entrega documentos entre las fechas data1 y data2
    #formato fecha data = AAAAMMDD
    ## ej. data1=20150101 data2=20170610 busca documentos entre el 01-01-2015 y 10-06-2017.
    return where + ' within "' + data1 + ' ' + data2 + '"'


def countryEPO(where='pn', country='WO'):
    # Criterio de busqueda de patentes de un pais en especifico
    return where + '=' + country


def proxEPO(where='ta', word1='green', word2='energy', dist=2, order='false'):
    #Criterio de busqueda de palabras a distancia espeficiada
    return where + '=' + word1 + ' prox/distance<=' + str(
        dist) + '/ordered=' + order + ' ' + where + '=' + word2


def andEPO(text1, text2):
    #concatena dos criterios de busqueda con el conector logico AND
    return text1 + ' and ' + text2


def orEPO(text1, text2):
    #concatena dos criterios de busqueda con el conector logico OR
    return text1 + ' or ' + text2
