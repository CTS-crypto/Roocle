from similarity import sim_docs_queries
import json

def _get_REL_rec():
    file=open('vecs_docs.json','r')
    docs=json.load(file)
    file.close()

    #carga los vectores de pesos de las consultas
    file=open('vecs_queries.json','r')
    queries=json.load(file)
    file.close()

    rec=sim_docs_queries(docs,queries,[0.08 for i in queries])

    file=open('med/MED.REL')
    
    REL=[0]*len(queries)
    for i in file.readlines():
        k=i.split()
        if REL[int(k[0])-1]==0:
            REL[int(k[0])-1]=set()
        
        if int(k[1])==0:
            REL[int(k[0])-1].add(int(k[2]))
        else:        
            REL[int(k[0])-1].add(int(k[1]))
    file.close()

    return REL,rec

def _precision(RR, REC):
    try:
        if REC==0:
            raise Exception()
        return RR/REC
    except (Exception):
        print("Cero Documentos recuperados. Division por cero")
        return 0

def _recall(RR, REL):
    try:
        if REL==0:
            raise Exception()
        return RR/REL

    except (Exception):
        print("Cero Documentos Relevantes. Division por cero")
        return 0

def _f_medida(RR, REL, REC, Beta):
    P = _precision(RR, REC)
    R = _recall(RR, REL)

    try:
        if Beta**2*P==-1*R:
            raise Exception()
        return ((1+ Beta**2)*P*R) / (Beta**2*P + R)

    except (Exception):
        print("Cero. Division por cero")
        return 0

def _f1_medida(RR, REL, REC):
    P = _precision(RR, REC)
    R = _recall(RR, REL)

    try:
        if P==-1*R:
            raise Exception()
        return (2*P*R)/(P+R)

    except (Exception):
        print("Cero. Division por cero")
        return 0

def _r_precision(RRr,r):
    try:
        if r==0:
            raise Exception()

        return RRr/r
    except (Exception):
        print("Division por cero")

def _fallout(RI,I):
    try:
        if I == 0:
            raise Exception()

        return RI/I
    except (Exception):
        print("Division por cero")

def precision():
    REL,rec=_get_REL_rec()

    REC=[]
    RR=[]
    precision=[]

    for i in rec:
        REC.append(set(i))
        

    for i in range(len(REC)):
        RR.append(REC[i].intersection(REL[i]))
        precision.append(_precision(len(RR[i]),len(REC[i])))

    return sum(precision)/len(precision)

def recall():
    REL,rec=_get_REL_rec()
    REC=[]
    RR=[]
    recall=[]

    for i in rec:
        REC.append(set(i))
        
    for i in range(len(REC)):
        RR.append(REC[i].intersection(REL[i]))
        recall.append(_recall(len(RR[i]),len(REL[i])))

    return sum(recall)/len(recall)

def f_medida(Beta):
    REL,rec=_get_REL_rec()

    REC=[]
    RR=[]
    f_medida=[]

    for i in rec:
        REC.append(set(i))
        
    for i in range(len(REC)):
        rr=REC[i].intersection(REL[i])
        RR.append(rr)
        f_medida.append(_f_medida(len(rr),len(REL[i]),len(REC[i]),Beta))

    return sum(f_medida)/len(f_medida)

def f1_medida():
    REL,rec=_get_REL_rec()

    REC=[]
    RR=[]
    f1_medida=[]

    for i in rec:
        REC.append(set(i))
        
    for i in range(len(REC)):
        RR.append(REC[i].intersection(REL[i]))
        f1_medida.append(_f1_medida(len(RR[i]),len(REL[i]), len(REC[i])))

    return sum(f1_medida)/len(f1_medida)

def fallout():
    REL,rec=_get_REL_rec()
    I=[]
    U=set(range(1,1400))

    for i in range(len(REL)):
        I.append(U.difference(REL[i]))

    REC=[]

    fallout=[]

    for i in range(len(rec)):
        REC.append(set(rec[i]))
        RI=0
        for j in rec[i]:
            if j in I[i]:
                RI+=1

            fallout.append(_fallout(RI,len(I)))

    return sum(fallout)/len(fallout)


    return 0

def r_fallout(r):
    REL,rec=_get_REL_rec()
    I=[]
    U=set(range(1,1400))

    for i in range(len(REL)):
        I.append(U.difference(REL[i]))

    REC=[]

    r_fallout=[]
    for i in range(len(rec)):
        REC.append(set(rec[i]))
        count=r
        RIr=0
        for j in rec[i]:
            if count==0:
                break
            
            if j in I[i]:
                RIr+=1
            count-=1
        r_fallout.append(_fallout(RIr,len(I)))

    return sum(r_fallout)/len(r_fallout)

def r_precision(r):
    REL,rec=_get_REL_rec()

    REC=[]
    r_precision=[]

    for i in range(len(rec)):
        count=r
        RRr=0
        for j in rec[i]:
            if count==0:
                break

            if j in REL[i]:
                RRr+=1
            count-=1
        r_precision.append(_r_precision(RRr,r))

    return sum(r_precision)/len(r_precision)

print('Precision promedio: ',precision())
print('Recobrado promedio: ',recall())
print('R_precision5 promedio: ',r_precision(5))
print('Medida_f0 promedio: ',f_medida(0))
print('Medida_f1 promedio: ',f_medida(1))
print('Medida_f2 promedio: ',f_medida(2))
print('Medida_f1 promedio: ',f1_medida())
print('fallout promedio: ',fallout())
print('R_fallout5 promedio: ',r_fallout(5))