import spacy
from spacy.cli import download
import nltk
from algorithm import BERT, word_embedding
from rouge import Rouge

# sentence scoring system p1 to p6 six different parameters to score a sentence
# p1 = özel isim
# p2 = sayısal değer
# p3 = node bağlantı kontrolü
# p4 = başlıktaki kelimeyi içeriyor mu
# p5 = kelime frekansı(tf-idf)
# p6 = Final score
DEBUG = False


# P1
def find_named_entities(document):
    print("P1 - Finding named entities")
    named_entities = []
    # for token in document:
    #     if token.pos_ == "PROPN":
    #         named_entities.append(token.text)
    for ent in document.ents:
        if ent.label_ == "PERSON" or ent.label_ == "ORG":
            named_entities.append(ent.text)
    # split named entities
    named_entities = [item for sublist in named_entities for item in sublist.split()]
    # find ratio
    named_entities_ratio = len(named_entities) / len(document)
    if DEBUG:
        print(named_entities)
        print(named_entities_ratio)
    return named_entities, named_entities_ratio


# P2
def find_numeric_values(document):
    print("P2 - Finding numeric values")
    numeric_values = []
    # Style 1

    for token in document:
        if token.like_num:
            numeric_values.append(token.text)

    # Style 2
    # for token in document:
    #     if token.like_num:
    #         tokentext = token.text
    #         if numeric_values:
    #             if numeric_values[-1].endswith(" " + tokentext):
    #                 continue
    #         while token.head.pos_ == "NUM":
    #             token = token.head
    #             tokentext = tokentext + " " + token.text
    #         numeric_values.append(tokentext)
    numeric_to_text_ratio = len(numeric_values) / len(document)
    if DEBUG:
        print(numeric_values)
        print(numeric_to_text_ratio)
    return numeric_values, numeric_to_text_ratio


# P3
def find_node_connections(node_scores, node_threshold, i):
    print("P3 - Finding node connections")
    number_of_nodes = len(node_scores)
    number_of_connections = 0
    for j in range(len(node_scores)):
        if i == j:
            continue
        if node_scores[i][j] > node_threshold:
            if DEBUG:
                print("Node " + str(i) + " is connected to Node " + str(j))
            number_of_connections += 1
    return number_of_connections / (number_of_nodes - 1), number_of_connections


# P4
def belongs_to_title(document, title):
    print("P4 - Belongs to title")
    amount_of_title_words = len(title)
    if amount_of_title_words == 0:
        return 0
    amount_of_title_words_in_document = 0
    for token in document:
        if token.text in title:
            amount_of_title_words_in_document += 1
    title_ratio = amount_of_title_words_in_document / amount_of_title_words
    if title_ratio > 1:
        title_ratio = 1
    if DEBUG:
        print(title_ratio)
    return title_ratio


# P5
def find_tf_idf(document, top_terms):
    print("P5 - Finding tf-idf")
    # Find most frequent words
    tf_idf = []
    for token in document:
        if token.text in top_terms:
            tf_idf.append(token.text)
    tf_idf_ratio = len(tf_idf) / len(document)
    if DEBUG:
        print(tf_idf)
        print(tf_idf_ratio)
    return tf_idf, tf_idf_ratio


def most_used_words(document):
    freq_dist = nltk.FreqDist([token.text for token in document if token.is_alpha])
    threshold = int(len(freq_dist) * 0.1)
    most_used = freq_dist.most_common(threshold)
    return [word for word, _ in most_used]


# P6
def calculate_final_score(named_entities_ratio, numeric_to_text_ratio, node_connections, title_ratio,
                          tf_idf_ratio, title):
    if len(title) == 0:
        named_entities_ratio = named_entities_ratio * 0.20
        numeric_to_text_ratio = numeric_to_text_ratio * 0.15
        node_connections = node_connections * 0.35
        title_ratio = title_ratio * 0
        tf_idf_ratio = tf_idf_ratio * 0.30
    else:
        named_entities_ratio = named_entities_ratio * 0.13
        numeric_to_text_ratio = numeric_to_text_ratio * 0.10
        node_connections = node_connections * 0.3
        title_ratio = title_ratio * 0.22
        tf_idf_ratio = tf_idf_ratio * 0.25

    final_score = named_entities_ratio + numeric_to_text_ratio + node_connections + title_ratio + tf_idf_ratio
    return final_score


def create_sentence_scores(doc, nlp, num_sentences, top_terms, title, node_connections, node_threshold):
    scores = [[0.0] * 6 for _ in range(num_sentences)]
    connection_count = [0] * num_sentences

    for i, sent in enumerate(doc.sents):
        clearsent = [token for token in sent if not token.is_stop and not token.is_punct]
        lemmatisedsent = [token.lemma_ for token in clearsent]
        lemmatised_doc = nlp(' '.join(lemmatisedsent))  # Convert the list back to a spaCy Doc object
        if DEBUG:
            print(clearsent)
            print(lemmatisedsent)
        print("Sentence " + str(i + 1) + ": " + str(sent))
        named_entities, scores[i][0] = find_named_entities(lemmatised_doc)
        numeric_values, scores[i][1] = find_numeric_values(lemmatised_doc)
        scores[i][2], connection_count[i] = find_node_connections(node_connections, node_threshold, i)
        scores[i][3] = belongs_to_title(lemmatised_doc, title)
        tf_idf, scores[i][4] = find_tf_idf(lemmatised_doc, top_terms)
        scores[i][5] = calculate_final_score(scores[i][0], scores[i][1],
                                             scores[i][2], scores[i][3],
                                             scores[i][4], title)
    return scores, connection_count


def start(text, title, node_threshold, summary_threshold, bert_selected):
    print("Starting summarisation: ", node_threshold, " - ", summary_threshold, " - ", bert_selected)
    # Check if the English model is installed
    if not spacy.util.is_package("en_core_web_sm"):
        download("en_core_web_sm")

    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    if text == title:
        title = ""

    # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # for entity in doc.ents:
    #     print(entity.text, entity.label_)

    # Removing transition phrases from the document
    cleardoc = [token for token in doc if not token.is_stop and not token.is_punct]
    lemmatised_fulldoc = [token.lemma_ for token in cleardoc]
    lemmatised_fulldoc = nlp(' '.join(lemmatised_fulldoc))  # Convert the list back to a spaCy Doc object

    num_sentences = len(list(doc.sents))

    top_terms = most_used_words(lemmatised_fulldoc)
    if DEBUG:
        print(top_terms)

    titledoc = nlp(title)
    cleartitle = [token for token in titledoc if not token.is_stop and not token.is_punct]
    lemmatised_title = [token.lemma_ for token in cleartitle]

    if bert_selected:
        node_connection_scores = BERT(text)
    else:
        node_connection_scores = word_embedding(text)

    # calculate the scores for each sentence
    sentence_scores, connection_count = create_sentence_scores(doc, nlp, num_sentences, top_terms, lemmatised_title,
                                                               node_connection_scores, node_threshold)
    sentences = list(doc.sents)
    summary_text = ""
    i = 0
    # Summary in the order of the sentences
    for score in sentence_scores:
        if score[5] > summary_threshold:
            # append the sentence to the summary_text
            summary_text += sentences[i].text + " "
        i += 1

    # Summary in the order of sentence scores
    # final_scores = [score[5] for score in sentence_scores]
    # sorted_scores = sorted(final_scores, reverse=True)
    # for score in sorted_scores:
    #     if score > summary_threshold:
    #         # append the sentence to the summary_text
    #         summary_text += sentences[final_scores.index(score)].text + " "
    print("Summary:\n" + summary_text)

    # print the scores for each sentence
    if DEBUG:
        for i in sentence_scores:
            # format the text to show 2 decimal places
            print("{:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f}".format(i[0], i[1], i[2], i[3], i[4], i[5]))
            print("connectioncount:" + str(connection_count[sentence_scores.index(i)]))
    return summary_text, sentences, sentence_scores, node_connection_scores, top_terms, connection_count


def calculate_rouge(summary, reference):
    rouge = Rouge()
    scores = rouge.get_scores(summary, reference)
    return scores


if __name__ == '__main__':
    DEBUG = True
    starttext = (
        "Sebastian and cars\n"
        "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the "
        "company took him seriously. “I can tell you very senior CEOs of major American car companies would shake "
        "my hand and turn away because I wasn’t worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")
    starttitle = starttext.split("\n")[0]
    starttext = starttext.replace(starttitle + "\n", "")
    starttext = starttext.replace("\n", " ")
    if DEBUG:
        print("title: " + starttitle)
        print("text: " + starttext)
    start(starttext, starttitle, 0.2, 0.2, False)
