from math import sqrt
import heapq
import json

#calcula la similitud entre un documento y una consulta
def sim_doc_query(doc,query):
    
    if len(doc)==0 or len(query)==0:
        return 0
        
    num=sum(doc[term]*query[term] for term in query if term in doc)
    
    den_1=sqrt(sum(doc[term]**2 for term in doc))
    
    den_2=sqrt(sum(query[term]**2 for term in query))
    
    return num/(den_1*den_2)

#calcula la similitud entre una consulta y cada documento de una coleccion, devolviendo de forma ordenada los m documentos mas similares a la consulta
def sim_docs_query(docs,query,m):
    
    heap=[]
    n=0
    
    for doc in docs:
        n+=1
        sim=sim_doc_query(doc, query)
        if sim >= m:
            heapq.heappush(heap, (sim,n))
    
    total=len(heap)
    index=total-1
    result=[0 for i in range(total)]
    
    for i in range(total):
        doc=heapq.heappop(heap)[1]
        result[index]=doc
        index-=1
        
    return result

#devuelve, para una lista de consultas, un numero especificado de documentos mas similares para cada consulta
def sim_docs_queries(docs,queries,min_sims):
    return [sim_docs_query(docs, query,m) for query,m in zip(queries,min_sims)]