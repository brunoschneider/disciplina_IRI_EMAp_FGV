# coding: utf-8

import glob
import whoosh.index as index
from whoosh.fields import Schema, TEXT, STORED
from whoosh.qparser import QueryParser


# gerando uma lista com a localização (path) dos arquivos a serem indexados
def caminhotxt(path):
    archives_list = []
    saida = []
    for fil in glob.glob(path):
        saida.append(fil)
    for x in sorted(saida):
        archives_list.append(x)
    return archives_list

#SCHEMA

# criando o schema
myschema = Schema(
    title=TEXT(stored=True),
    content=TEXT(spelling=True),
    path=STORED
)
lista_arquivos = caminhotxt('indexdir/*.txt')


#INDEX 

# criando o indice
ix = index.create_in("indexdir", myschema)

# abrindo um indice ja existente
#ix = index.open_dir("indexdir")

for elements in range(len(lista_arquivos)):
    text_open = open(lista_arquivos[elements])
    text = text_open.read()
    nome_arq = lista_arquivos[elements].strip('indexdir')
    with ix.writer() as w:
        # adicionando arquivos ao indice    
        w.add_document(title=nome_arq.decode('utf8'), content=text.decode('utf8'))
    
#SEARCH
with ix.searcher() as searcher:
    # realizando a busca pelo conteúdo dos arquivos especificando um determinado termo
    query = QueryParser("content", ix.schema).parse(u'war')
    results = searcher.search(query)
    
    # imprimindo os resultados
    print '*** RESULTADOS ***'
    print 'numero de documentos encontrados:', len(results)
    print 'TOP 5:'    
    for x in range(5):
        print results[x]




