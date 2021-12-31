import json


dict = {}

def select_action(json_request):

    json_data = json.loads(json_request)

    if json_data['action'] == 'add_term':
        add_term(json_data['data'])

    elif json_data['action'] == 'terms':
        return terms_in_doc(json_data['key'])

    elif json_data['action'] == 'terms_frec':
        return terms_in_doc_frec(json_data['key'])

    elif json_data['action'] == 'get':
        return get(json_data['key'])


def add_term(data):
    for elem in data:
        key = elem['key']
        value = elem['value']
        dict[key] = value

def get(key):
    response = {}

    if key in dict:
        response['success'] = True
        response['value'] = dict[key]
    else:
        response['success'] = False
        response['value'] = None

    return json.dumps(response)


def terms_in_doc(doc):
    response = {}
    terms = [term for term in dict if (doc in dict[term]['documents'])]
    response['terms'] = terms

    return json.dumps(response)

def terms_in_doc_frec(doc):
    response = {}
    terms = [(term, dict[term]['documents'][doc]['tf']) for term in dict if (doc in dict[term]['documents'])]
    response['terms'] = terms

    return json.dumps(response)
