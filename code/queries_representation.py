import json
from docs_representation import calculate_tfijs
from queries_preprocess import queries_preprocessing

#calcula los vectores de pesos para las consultas
def calculate_weigths_queries(a,idfs,terms_freq):
    
    vecs_queries=[]
    
    for tfj in calculate_tfijs(terms_freq):
        vec_weigths={}
        for term in tfj:
            vec_weigths[term]=(a+(1-a)*tfj[term])*idfs[term]
        vecs_queries.append(vec_weigths)
        
    return vecs_queries

if __name__=='__main__':
    
    #carga las idf
    file=open("idfs.json","r")
    idfs=json.load(file)
    file.close()
    
    collection='med/MED.QRY'
    
    vecs_queries=calculate_weigths_queries(0.5, idfs, queries_preprocessing(collection,idfs))

    #guarda los vectores de pesos para las consultas
    with open('vecs_queries.json','w') as fout:
        json.dump(vecs_queries, fout)