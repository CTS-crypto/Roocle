def sum(vec1,vec2):
    sum={}
    for i in vec1.keys():
        if i in vec2:
            sum[i]=vec1[i]+vec2

        else:
            sum[i]=vec1[i]

    for i in vec2.keys():
        if not (i in sum):
            sum[i]=vec2[i]

def mult(vec,k):
    mult={}
    for i in vec.keys():
        mult[i]=k*vec[i]

def Rocchio(query,docs_rel,docs_no_rel,alpha,beta,ganma):
    Doc_rel={}
    for i in docs_rel:
        Docs_rel=sum(Docs_rel,i)

    Docs_rel=mult(Docs_rel,(beta*(1/len(docs_rel))))

    Doc_no_rel={}
    for i in docs_no_rel:
        Doc_no_rel=sum(Doc_no_rel,i)

    Doc_no_rel=mult(Doc_no_rel,(ganma*(1/len(docs_no_rel))))

    doc=sum(Doc_rel,mult(Doc_no_rel,-1))
    qm=sum(mult(query,alpha),doc)
    return qm