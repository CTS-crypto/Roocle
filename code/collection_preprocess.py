import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

'''
    CC coordinating conjunction
    CD cardinal digit
    DT determiner
    EX existential there (like: “there is” … think of it like “there exists”)
    FW foreign word
    IN preposition/subordinating conjunction
    JJ adjective ‘big’
    JJR adjective, comparative ‘bigger’
    JJS adjective, superlative ‘biggest’
    LS list marker 1)
    MD modal could, will
    NN noun, singular ‘desk’
    NNS noun plural ‘desks’
    NNP proper noun, singular ‘Harrison’
    NNPS proper noun, plural ‘Americans’
    PDT predeterminer ‘all the kids’
    POS possessive ending parent’s
    PRP personal pronoun I, he, she
    PRP$ possessive pronoun my, his, hers
    RB adverb very, silently,
    RBR adverb, comparative better
    RBS adverb, superlative best
    RP particle give up
    TO, to go ‘to’ the store.
    UH interjection, errrrrrrrm
    VB verb, base form take
    VBD verb, past tense took
    VBG verb, gerund/present participle taking
    VBN verb, past participle taken
    VBP verb, sing. present, non-3d take
    VBZ verb, 3rd person sing. present takes
    WDT wh-determiner which
    WP wh-pronoun who, what
    WP$ possessive wh-pronoun whose
    WRB wh-abverb where, when
'''

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

#Preprocesamineto de la coleccion. Devuelve un diccionario tal que la llave es el termino y el valor son los documentos en los que aparece el termino
def collection_preprocessing(collection):
    file=open(collection)
    term_docs={}
    actual_document=0
    for line in file:
        if line[1]=='I':
            actual_document+=1
        elif line[1]=='T' or line[1]=='W'or line[1]=='A' or line[1]=='B':
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
                if gramatical_root not in stop_words:
                    if gramatical_root in term_docs:
                        term_docs[gramatical_root].add(actual_document)
                    else:
                        term_docs[gramatical_root]=set([actual_document])
    file.close()
    return term_docs,actual_document

#Preprocesamiento de la coleccion. Deveulve de forma perezosa un diccionario por cada documento que indica la frecuencia de cada termino el documento, ademas se devuelve un entero que representa la frecuencia maxima de un termino en el documento
def terms_freq_doc(collection):
    file=open(collection)
    document_terms_freq=None
    max_freq=0
    for line in file:
        if line[1]=='I':
            if document_terms_freq!=None:
                yield document_terms_freq,max_freq
            document_terms_freq={}
            max_freq=0
        elif line[1]=='T' or line[1]=='W'or line[1]=='A' or line[1]=='B':
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
                if gramatical_root not in stop_words:
                    if gramatical_root in document_terms_freq:
                        document_terms_freq[gramatical_root]+=1
                    else:
                        document_terms_freq[gramatical_root]=1
                    max_freq=max(max_freq,document_terms_freq[gramatical_root])
    yield document_terms_freq,max_freq
    file.close()
    
def limits_documents(collection):
    file=open(collection)
    
    limits=[]
    in_document=False  
    index=0
    inicial=0
    first_taken=False
    
    for line in file:
        if line[1]=='W':
           inicial=index+1
           first_taken=True
        elif line[1]=='I' and first_taken:
            limits.append((inicial,index-1))
        index+=1
    limits.append((inicial,index-1))
    
    file.close()
        
    return limits