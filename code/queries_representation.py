import json
from docs_representation import calculate_tfijs
from queries_preprocess import queries_preprocessing,cran_recovered_documents

#carga las idf
file=open("idfs.json","r")
idfs=json.load(file)
file.close()

#calcula los vectores de pesos para las consultas
def calculate_weigths_queries(a,idfs,terms_freq):
    
    vecs_queries=[]
    
    for tfj in calculate_tfijs(terms_freq):
        vec_weigths={}
        for term in tfj:
            if term in idfs:
                vec_weigths[term]=(a+(1-a)*tfj[term])*idfs[term]
        vecs_queries.append(vec_weigths)
        
    return vecs_queries

vecs_queries=calculate_weigths_queries(0.5, idfs, queries_preprocessing())
recovered_documents=cran_recovered_documents()

#guarda los vectores de pesos para las consultas
with open('vecs_queries.json','w') as fout:
    json.dump(vecs_queries, fout)

#guarda la cantidad de documentos que se deben recuperar para cada consulta    
with open('recovered_documents.json','w') as fout:
    json.dump(recovered_documents, fout)