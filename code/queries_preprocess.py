import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

tags_code={
    'NN':'n',
    'NNS':'n',
    'NNP':'n',
    'NNPS':'n',
    'VB':'v',
    'VBD':'v',
    'VBG':'v',
    'VBN':'v',
    'VBP':'v',
    'VBZ':'v',
    'JJ':'a',
    'JJR':'a',
    'JJS':'a',
    'RB':'r',
    'RBR':'r',
    'RBS':'r'
}

stop_words=set(stopwords.words("english"))

lemmatizer=WordNetLemmatizer()

#procesa consulta individual
def query_preprocessing(query,idfs):
    
    query_terms_freq={}
    max_freq=0
    words=word_tokenize(query)
    tagged=nltk.pos_tag(words)
    
    for item in tagged:
        if item[0]=='.' or item[0]==',' or item[0]=='?' or item[0]=='!' or item[1]=='POS':
            continue
        if item[1] in tags_code:
            gramatical_root=lemmatizer.lemmatize(item[0],tags_code[item[1]])
        else:
            gramatical_root=lemmatizer.lemmatize(item[0])
        if gramatical_root not in stop_words and gramatical_root in idfs:
            if gramatical_root in query_terms_freq:
                query_terms_freq[gramatical_root]+=1
            else:
                query_terms_freq[gramatical_root]=1
            max_freq=max(max_freq,query_terms_freq[gramatical_root])
    
    return query_terms_freq,max_freq
    

#Preprocesamiento de las consultas. Devuele un diccionario por cada consulta que indica la fecuencia de cada termino en la consulta, ademas de un entero que indica a frecuencia maxima de un termino en la consulta 
def queries_preprocessing(idfs):
    file=open("cran/cran.qry")
    query_terms_freq=None
    max_freq=0
    for line in file:
        if line[1]=='I':
            if query_terms_freq!=None:
                yield query_terms_freq,max_freq
            query_terms_freq={}
            max_freq=0
        elif line[1]=='W':
            continue
        else:
            words=word_tokenize(line)
            tagged=nltk.pos_tag(words)
            for item in tagged:
                if item[0]=='.' or item[0]==',' or item[0]=='?' or item[0]=='!' or item[1]=='POS':
                    continue
                if item[1] in tags_code:
                    gramatical_root=lemmatizer.lemmatize(item[0],tags_code[item[1]])
                else:
                    gramatical_root=lemmatizer.lemmatize(item[0])
                if gramatical_root not in stop_words and gramatical_root in idfs:
                    if gramatical_root in query_terms_freq:
                        query_terms_freq[gramatical_root]+=1
                    else:
                        query_terms_freq[gramatical_root]=1
                    max_freq=max(max_freq,query_terms_freq[gramatical_root])
    yield query_terms_freq,max_freq
    file.close()
 
#devuelve una lista que indica cuantos documentos se deben devolver para cada consulta    
def cran_recovered_documents():
    file=open("cran/cranqrel")
    actual=0
    recovered_documents=[]
    for line in file:
        items=line.split()
        if int(items[0])!=actual:
            actual+=1
            recovered_documents.append(1)
        else:
            recovered_documents[actual-1]+=1
    return recovered_documents