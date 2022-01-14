def sum(vec1,vec2):
    for i in vec2:
        if i in vec1:
            vec1[i]+=vec2[i]

        else:
            vec1[i]=vec2[i]
			
	return vec1

def mult(vec,k):
    mult={}
    for i in vec:
        mult[i]=k*vec[i]

def Rocchio(query,docs_rel,docs_no_rel,alpha,beta,ganma):
    Doc_rel={}
    for i in docs_rel:
        Doc_rel=sum(Doc_rel,i)

    Doc_rel=mult(Doc_rel,(beta*(1/len(docs_rel))))

    Doc_no_rel={}
    for i in docs_no_rel:
        Doc_no_rel=sum(Doc_no_rel,i)

    Doc_no_rel=mult(Doc_no_rel,(ganma*(1/len(docs_no_rel))))

    doc=sum(Doc_rel,mult(Doc_no_rel,-1))
    qm=sum(mult(query,alpha),doc)
    return qm