from flask import Flask, render_template, request
import re
import math

app = Flask(__name__)

def formula1(length,term_frequeny):
    #formula1 implementation here
    value=term_frequeny
    numerator=length-value+0.5
    denominator=value+0.5
    return math.log2(numerator/denominator)

def formula2(length,term_frequeny):
    #formula2 implementation here
    value=term_frequeny
    numerator=length+0.5
    denominator=value+0.5
    return math.log2(numerator/denominator)

def split_documents_into_words(documents):
    split_documents = {}
    for i, doc in documents.items():
        words = re.findall(r'\b\w+\b|"\w+\s\w+"|"\w+"', doc)
        flattened_words = [word for phrase in words for word in (phrase.split() if '"' in phrase else [phrase])]
        lowercase_list = [word.lower() for word in flattened_words]
        split_documents[i] = lowercase_list
    return split_documents

def term_document_frequency(split_documents, query):
    term_docuement_frequency = {}
    query_words = re.findall(r'\w+', query.lower())
    for word in query_words:
        count = 0
        for i in split_documents:
            if word in split_documents[i]:
                count += 1
        term_docuement_frequency[word] = count
    return term_docuement_frequency

def negative_weights(split_documents, query, term_docuement_frequency):
    # Your negative_weights implementation here
    document_rank = {}
    query_words=re.findall(r'\w+',query.lower())
    for i in split_documents:
        value=0
        for word in query_words:
            if word in split_documents[i]:
                value=value+formula2(len(split_documents),term_docuement_frequency[word])
        document_rank[i]=value
    return document_rank

def document_ranking(split_documents, query, term_docuement_frequency):
    document_rank = {}
    query_words = re.findall(r'\w+', query.lower())
    for i in split_documents:
        value = 0
        for word in query_words:
            if word in split_documents[i]:
                value += formula1(len(split_documents),term_docuement_frequency[word])
                if value < 0:
                    result = negative_weights(split_documents, query, term_docuement_frequency)
                    return result
        document_rank[i] = value
    return document_rank

@app.route('/', methods=['POST', 'GET'])
def calculate():
    documents = {}
    query = ""
    document_rank = {}

    if request.method == 'POST':
        num_documents = int(request.form.get('numDocuments'))

        for i in range(1, num_documents + 1):
            document = request.form.get(f'document{i}', '')
            documents[i] = document

        query = request.form.get('query', '')

        split_documents = split_documents_into_words(documents)
        term_docuement_frequency = term_document_frequency(split_documents, query)
        document_rank = document_ranking(split_documents, query, term_docuement_frequency)

    return render_template('index.html', documents=documents, query=query, document_rank=document_rank)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')