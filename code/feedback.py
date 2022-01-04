from queries_preprocess import*
import json
import internal_json


def relevance_feedback(documents):
    relevant_words = set()

    for doc in documents:
        json_request=json.dumps({'action': 'terms_frec', 'key': doc})
        json_response=json.loads(internal_json.select_action(json_request)) 
        lista=json_response['terms']
        lista.sort(key=lambda x: x[1], reverse=True)
        relevant_words.add(lista[0][0])

    return " ".join(list(relevant_words))

