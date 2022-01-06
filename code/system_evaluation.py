import similarity as sim
import json

def _get_REL_rec():
    file=open('vecs_docs.json','r')
    docs=json.load(file)
    file.close()

    #carga los vectores de pesos de las consultas
    file=open('vecs_queries.json','r')
    queries=json.load(file)
    file.close()

    #carga la cantidad de documentos que se deberan recuperar para cada consulta
    file=open('recovered_documents.json','r')
    recovered_documents=json.load(file)
    file.close()
    rec=sim.sim_docs_queries(docs,queries,recovered_documents)

    file=open('cran/cranqrel')
    
    REL=[0]*len(queries)
    for i in file.readlines():
        k=i.split()
        if REL[int(k[0])-1]==0:
            REL[int(k[0])-1]=set()
            
        REL[int(k[0])-1].add(int(k[1]))
    file.close()

    return [REL,rec]

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
    REL_rec=_get_REL_rec()
    REL=REL_rec[0]
    rec=REL_rec[1]

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
    REL_rec=_get_REL_rec()
    REL=REL_rec[0]
    rec=REL_rec[1]
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
    REL_rec=_get_REL_rec()
    REL=REL_rec[0]
    rec=REL_rec[1]

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
    REL_rec=_get_REL_rec()
    REL=REL_rec[0]
    rec=REL_rec[1]

    REC=[]
    RR=[]
    f1_medida=[]

    for i in rec:
        REC.append(set(i))
        
    for i in range(len(REC)):
        RR.append(REC[i].intersection(REL[i]))
        f1_medida.append(_f1_medida(len(RR[i]),len(REL[i]), len(REC[i])))

    return sum(f1_medida)/len(f1_medida)

def fallout(r):
    REL_rec=_get_REL_rec()
    REL=REL_rec[0]
    rec=REL_rec[1]
    I=[]
    U=set(range(1,1400))

    for i in range(len(REL)):
        I.append(U.difference(REL[i]))

    REC=[]
    RR=[]
    fallout=[]
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
        fallout.append(_fallout(RIr,len(I)))

    return sum(fallout)/len(fallout)

def r_precision(r):
    REL_rec=_get_REL_rec()
    REL=REL_rec[0]
    rec=REL_rec[1]

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

print(f_medida(10)) #p=0.2112299630965942 r=0.2112299630965942