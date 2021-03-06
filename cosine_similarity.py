
def get_doc_length(weights:[int]) -> float:
    ''' Given the list of wt values (query or doc), calculate the normalized value '''
    val = 0
    for n in weights:
        val += n ** 2
    doc_length = sqrt(val)
    return doc_length

def get_query_tfidf_vectors(query : [str]) -> dict:
    ''' Calcuates ALL tf-idf vectors for the given query token.
        Includes normalize value
        key = token | value = tf-idf vector
    '''
    global QUERY_POSTINGS
    result = OrderedDict()
    weights = list()
    word_freq = computeWordFrequency(query)

    ''' Calculate the vector (except for normalized value) '''
    for token in query:
        if token not in result:
            df = len(QUERY_POSTINGS[token])
            tf_wt = 1+log10(word_freq[token])
            idf = log10(55_393 / df)
            wt = tf_wt * idf
            tfidf_vector = {
                "wt" : wt,
                "normalize" : 0,
            }
            weights.append(wt)
            result[token] = tfidf_vector

    ''' Calculate normalized value '''
    doc_length = get_doc_length(weights)
    for token in result:
        result[token]["normalize"] = result[token]["wt"] / doc_length

    return result

def get_doc_posting(token : str, docID : int) -> list:
    ''' Get the posting for the given token and docID
    '''
    global QUERY_POSTINGS
    for posting in QUERY_POSTINGS[token]:
        if posting[0] == docID:
            return posting
    return []

def get_document_tfidf_vector(token : str, docID : int) -> dict:
    ''' Calculates the weighted tf-idf vector for the given token.
        Still need to calculate "normalize" value
        Token should already be stemmed
    '''
    posting = get_doc_posting(token, docID)
    tf_raw = len(posting) - 2
    tf_wt = 1+log10(tf_raw)

    result = {
        "wt" : tf_wt, 
        "normalize" : 0,
        } 
    
    return result

# def get_doc_vectors(query_tokens : [str]) -> dict:
#     ''' Given the list of stemmed query tokens,
#         Calculate doc vectors for cosin similarity scoring
#     '''
#     global QUERY_POSTINGS
#     doc_vectors = dict()
#     for token in query_tokens:
#         for posting in QUERY_POSTINGS[token]:
#             docID = posting[0]
#             vector = get_document_tfidf_vector(token, docID)
#             if docID not in doc_vectors:
#                 doc_vectors[docID] = {token : vector}
#             else:
#                 doc_vectors[docID][token] = vector
#     return doc_vectors

def get_doc_vectors(query_tokens : [str]) -> [int]:
    ''' Given the list of stemmed query tokens,
        Calculate doc vectors for cosin similarity scoring
    '''
    global QUERY_POSTINGS
    doc_vectors = list()
    for token in query_tokens:
        for posting in QUERY_POSTINGS[token]:
            docID = posting[0]
            vector = get_document_tfidf_vector(token, docID)
            if docID not in doc_vectors:
                doc_vectors[docID] = {token : vector}
            else:
                doc_vectors[docID][token] = vector
    return doc_vectors

def normalize_doc_wts(doc_vectors : dict): 
    ''' 
    {
        token : vector dict,
        token : vector dict
    }
    '''
    weights = list()
    weights = [doc_vectors[token]["wt"] for token in doc_vectors]
    
    doc_length = get_doc_length(weights)

    for token in doc_vectors:
        doc_vectors[token]["normalize"] = doc_vectors[token]["wt"] / doc_length
    
    return doc_vectors


def process_query(query : [str]) -> dict:
    ''' Returns a dict of docIDs and their scores. Query tokens should already be stemmed
    '''
    start = perf_counter()
    start = time()
    ''' calculate query vector '''
    # dict of vectors for each unique token in query
    query_tfidf_vector = get_query_tfidf_vectors(query) 
    print("query vector", query_tfidf_vector)
    ''' calculate doc vectors '''
    # docID : {
    #     "token1" : {vector dict},
    #     "token2" : {vector dict}, ...
    # }
    
    doc_vectors = get_doc_vectors(query) 

    ''' Normalize doc vector weights '''
    for docID in doc_vectors:
        doc_vectors[docID] = normalize_doc_wts(doc_vectors[docID])
    ''' Calculate scores ''' 
    scores = dict()
    for docID in doc_vectors:
        score = 0
        for token in query_tfidf_vector:
            if token in doc_vectors[docID]:         
                score += doc_vectors[docID][token]["normalize"] * query_tfidf_vector[token]["normalize"]
        scores[docID] = score
    print("scores type {}".format(type(scores)))
    # scores = sorted(scores.items(), key=lambda x:x[1])
    end = time()
    # print("Search time elapsed: {} ms".format( (perf_counter()) - start * 1000))
    print("Search time elapsed: {} ms".format( (end-start) * 1000))
    return scores

def process_query2(query: [str]) -> {int : float}:
    global QUERY_POSTINGS

 
    scores = dict()
    
    score = dict() # doc id : weight(s)
    for t in query:
        for p in QUERY_POSTINGS[t]:
            doc_id = p[0]
            wt_d = 1+log10(len(p)-3) 
            if doc_id in length:
                length[doc_id] += wt_d ** 2
            else:
                length[doc_id] = wt_d ** 2
        for p in QUERY_POSTINGS[t]:
            doc_id = p[0]
            wf_td = 1+log10(len(p) - 3)
            length[doc_id] = wf_td / sqrt(length[doc_id])
    
    for i in range(len(query)):
        wt_q = query.count(query[i])
        for j in QUERY_POSTINGS[query[i]]:
            # wf(t,d)
            scores[i+j] += 
    
    for i in range(len(scores)):
        scores[i] /= length[i]
    
    return scores

def query_doc_count():
''' Returns the number of documents query retrieved '''
    global QUERY_POSTINGS
    doc_count = 0
    for key in QUERY_POSTINGS:
        doc_count += len(QUERY_POSTINGS[key])
    return doc_count