from math import log10
from collection_preprocess import collection_preprocessing,terms_freq_doc,limits_documents
import json

#calcula idf
def calculate_idfs(preprocessing):
    term_docs,total=preprocessing
    idfs={}
    for term in term_docs:
        idfs[term]=log10(total/len(term_docs[term]))
    return idfs

#calcula tf de forma perezosa
def calculate_tfijs(terms_freq_doc):
    for freq,max_freq in terms_freq_doc:
        tfj={}
        for term in freq:
            tfj[term]=freq[term]/max_freq
        yield tfj

#calcula los vectores de pesos de los documentos
def calculate_weigths(terms_freq_doc,idfs):
    
    vecs_docs=[]
    
    for tfj in calculate_tfijs(terms_freq_doc):
        vec_weigths={}
        for term in tfj:
            vec_weigths[term]=tfj[term]*idfs[term]
        vecs_docs.append(vec_weigths)
        
    return vecs_docs

if __name__=='__main__':
    
    collection="med/MED.ALL"
    
    idfs=calculate_idfs(collection_preprocessing(collection))
    vecs_docs=calculate_weigths(terms_freq_doc(collection),idfs)
    limits=limits_documents(collection)

    #guarda los pesos
    with open('vecs_docs.json','w') as fout:
        json.dump(vecs_docs, fout)

    #guarda los idfs
    with open('idfs.json','w') as fout:
        json.dump(idfs, fout)
        
    #guarda los limites de los documentos
    with open('limits.json','w') as fout:
        json.dump(limits, fout)