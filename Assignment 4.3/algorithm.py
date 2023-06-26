
#import nltk
#nltk.download('stopwords')
import re
import numpy as np
from numpy.linalg import norm
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english")

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

from gensim.models import Word2Vec


def get_text(doc):

    filtered_text = []
    # f = open("example.txt","r", encoding="utf8")
    # lines = f.readlines()
    lines = doc.split("\n")

    filtered_line = []

    for i in lines:
        if(i != '\n'):
            filtered_line.append(i.split("\n")[0])

    filtered_sentences = []

    for line in filtered_line:
        for i in re.split(r'(?<=[.!?])\s+', line):
            if(i != ''):
                i = tokenizer.tokenize(i)
                filtered_sentences.append(' '.join(i))


    print(filtered_sentences)
    return filtered_sentences


def word_embedding(text):
    filtered_text = []
    # f = open("example.txt","r")
    # lines = f.readlines()
    lines = text.split("\n")

    filtered_line = []

    for i in lines:
        if(i != '\n'):
            filtered_line.append(i.split("\n")[0])

    filtered_sentences = []

    for line in filtered_line:
        for i in re.split(r'(?<=[.!?])\s+', line):
            if(i != ''):
                i = tokenizer.tokenize(i)
                filtered_sentences.append(' '.join(i))

    #filtered_sentences.pop() Bazı koşullarda lazım olabilir

    filtered_word = []

    for sentence in filtered_sentences:
        tokenized_text = sentence.split()
        words = [word for word in tokenized_text if word.lower() not in stop_words]
        filtered_word.append(words)

    print(filtered_word)

    model = Word2Vec(filtered_word, min_count=1)

    scores = []

    for sentence in filtered_word:
        sentence_score = 0
        for word in sentence:
            #sentence_score += model.wv[word]
            sentence_score = np.add( model.wv[word],sentence_score)
        scores.append(sentence_score)

    #print(scores)

    semantic_similarity_ratio = []

    for i in range(len(scores)):
        ratio = []
        for j in range(len(scores)):
            cos_sim = np.dot(scores[i], scores[j]) / (norm(scores[i]) * norm(scores[j]))
            ratio.append(cos_sim)
        semantic_similarity_ratio.append(ratio)


    # cos_sim = np.dot(scores[12], scores[13]) / (norm(scores[12]) * norm(scores[13]))
    print(semantic_similarity_ratio)

    return semantic_similarity_ratio



def BERT(doc):


    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    text = get_text(doc)

    # Cümleleri BERT modeli için girişe uygun hale getir
    input_ids = []
    for sentence in text:
        tokens = tokenizer.encode(sentence, add_special_tokens=True)
        input_ids.append(tokens)

    # En uzun cümle uzunluğunu bul
    max_length = max(len(sentence) for sentence in input_ids)

    # Cümleleri doldurarak aynı uzunluğa getir
    padded_input_ids = []
    for sentence in input_ids:
        padded_sentence = sentence + [tokenizer.pad_token_id] * (max_length - len(sentence))
        padded_input_ids.append(padded_sentence)

    # PyTorch tensorına dönüştür
    input_tensors = torch.tensor(padded_input_ids)

    # BERT modelini kullanarak cümleleri kodla
    outputs = model(input_tensors)

    # Kodlanmış vektörleri al
    encoded_layers = outputs.last_hidden_state.detach().numpy()

    # Kosinüs benzerliğini hesapla
    #similarities = cosine_similarity(encoded_layers[:, 0], encoded_layers[:, 1])

    # Benzerlik sonuçlarını yazdır
    #for i, similarity in enumerate(similarities):
    #    print(f"Cümle {i+1} ve Cümle {i+2} arasındaki benzerlik:", similarity)

    semantic_similarity_ratio = []
    for i in range(len(encoded_layers)):
        ratio = []
        for j in range(len(encoded_layers)):
            similarity = cosine_similarity(encoded_layers[i].reshape(1, -1), encoded_layers[j].reshape(1, -1))
            ratio.append(similarity[0][0])
            print(f"{i+1}. cümle ile {j+1}. cümle arasındaki benzerlik:", similarity[0][0])
        semantic_similarity_ratio.append(ratio)

    print(semantic_similarity_ratio)
    return semantic_similarity_ratio








# print("BERT:", BERT())

#get_text()
#word_embedding()
