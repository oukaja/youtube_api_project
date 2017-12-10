# dependencies
from __future__ import unicode_literals
import isodate
import requests
from hammock import Hammock as GendreAPI
from textblob import TextBlob
from string import punctuation
from collections import Counter
import re
from bidi.algorithm import get_display
import arabic_reshaper
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.util import ngrams
from pandas import DataFrame
import matplotlib.pyplot as plt
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['modyoutubeproject']
collection = db['commentaires']

# YouTube api key
api_key = "AIzaSyDt0lPqnHIgW8wcEI_Xzt5ifdYRAivn2og"

# Gender API
gendre = GendreAPI("http://api.namsor.com/onomastics/api/json/gendre")

# Video id
VIDEO_ID = "mn6Ia5e_suY"

# Max Results
MAX_RESULT = "50"

# get all info of videos
video_info = []

# get all comments
video_comments = []

# get all comments replies
video_comments_replies = []

snippet_c = list()
snippet_c_replies = list()

snippet = ""
contentDetails = ""
statistics = ""


# set id video
def id_video(id=""):
    global VIDEO_ID
    VIDEO_ID = id
    recharger_les_donnees()
    commentaire_vers_mongodb()


def recharger_les_donnees():
    global snippet, contentDetails, statistics, video_info, video_comments
    # Google API
    url_video_comments = "https://www.googleapis.com/youtube/v3/commentThreads?key=%s&textFormat=plainText&part=snippet,replies&videoId=%s&maxResults=%s" % (
        api_key,
        VIDEO_ID,
        MAX_RESULT)
    url_video_info = "https://www.googleapis.com/youtube/v3/videos?key=%s&part=snippet,contentDetails,statistics&id=%s&maxResults=%s" % (
        api_key,
        VIDEO_ID,
        MAX_RESULT)
    # get Data
    video_info = requests.get(url_video_info).json()
    video_comments = requests.get(url_video_comments).json()
    for i in range(0, len(video_info["items"])):
        video_item = video_info["items"]
        try:
            snippet = video_item[i]["snippet"]
            contentDetails = video_item[i]["contentDetails"]
            statistics = video_item[i]["statistics"]
        except:
            continue
    for i in range(0, len(video_comments["items"])):
        video_comment_item = video_comments["items"]
        try:
            snippet_c.append(video_comment_item[i]["snippet"])
            snippet_c_replies.append(video_comment_item[i]["replies"]["comments"])
        except:
            continue


def nettoyer_la_phrase(phrase):
    phrase = re.sub(r"(?:\@|https?\://)\S+|\n+", "", phrase.lower())
    sent = TextBlob(phrase)
    sent.correct()
    clean = ""
    for sentence in sent.sentences:
        words = sentence.words
        words = [''.join(c for c in s if c not in punctuation) for s in words]
        words = [s for s in words if s]
        clean += " ".join(words)
        clean += ". "
    return clean


def commentaire_vers_mongodb():
    commentaires = list()
    for snippet_c_user in snippet_c:
        commentaires.append(snippet_c_user["topLevelComment"]["snippet"]["textDisplay"])
    commentaires = (nettoyer_la_phrase(p) for p in commentaires)
    for commentaire in commentaires:
        comment = {"comment": commentaire}
        collection.insert(comment)


def commentaire_de_mongodb():
    comments = list()
    col = db.get_collection("commentaires")
    for document in col.find({}):
        comments.append(document['comment'])
    return comments


def video_info_comments():
    # snippet
    print("-------------------------------------------------------------------")
    print("snippet attributs")
    print("channel Id : " + snippet["channelId"])
    print("published At : " + snippet["publishedAt"])
    print("title : " + snippet["title"])
    print("description : " + snippet["description"])
    print("channel Title : " + snippet["channelTitle"])
    print("category Id : " + snippet["categoryId"])
    print("tags : ")
    for tag in snippet["tags"]:
        print("\t" + tag)
    print("-------------------------------------------------------------------")

    # contentDetails
    print("-------------------------------------------------------------------")
    print("contentDetails attributs")
    print("duration : " + str(isodate.parse_duration(contentDetails["duration"])))
    print("dimension : " + contentDetails["dimension"])
    print("-------------------------------------------------------------------")

    # statistics
    print("-------------------------------------------------------------------")
    print("statistics attributs")
    print("viewCount : " + statistics["viewCount"])
    print("likeCount : " + statistics["likeCount"])
    print("dislikeCount : " + statistics["dislikeCount"])
    print("commentCount : " + statistics["commentCount"])
    print("-------------------------------------------------------------------")

    # snippet comment
    print("-------------------------------------------------------------------")
    print("snippet comments")
    print("\t-------------------------------------------------------------------")
    for snippet_c_user in snippet_c:
        print("\tauthorDisplayName : " + snippet_c_user["topLevelComment"]["snippet"]["authorDisplayName"])
        print("\tauthorProfileImageUrl : " + snippet_c_user["topLevelComment"]["snippet"]["authorProfileImageUrl"])
        print("\tauthorChannelUrl : " + snippet_c_user["topLevelComment"]["snippet"]["authorChannelUrl"])
        print("\tauthorChannelId : " + snippet_c_user["topLevelComment"]["snippet"]["authorChannelId"]["value"])
        print("\ttextDisplay : " + snippet_c_user["topLevelComment"]["snippet"]["textDisplay"])
        print("\ttextOriginal : " + snippet_c_user["topLevelComment"]["snippet"]["textOriginal"])
        print("\tlikeCount : " + str(snippet_c_user["topLevelComment"]["snippet"]["likeCount"]))
        print("\tpublishedAt : " + snippet_c_user["topLevelComment"]["snippet"]["publishedAt"])
        print("\tcanReply : " + str(snippet_c_user["canReply"]))
        print("\ttotalReplyCount : " + str(snippet_c_user["totalReplyCount"]))
        print("\tisPublic : " + str(snippet_c_user["isPublic"]))
        print("\t-------------------------------------------------------------------")
    print("\t\t-------------------------------------------------------------------")

    for k in range(snippet_c_replies.__len__()):
        reply = snippet_c_replies[k][0]
        print("\t\tauthorDisplayName : " + reply["snippet"]["authorDisplayName"])
        print("\t\tauthorProfileImageUrl : " + reply["snippet"]["authorProfileImageUrl"])
        print("\t\tauthorChannelUrl : " + reply["snippet"]["authorChannelUrl"])
        print("\t\tauthorChannelId : " + reply["snippet"]["authorChannelId"]["value"])
        print("\t\ttextDisplay : " + reply["snippet"]["textDisplay"])
        print("\t\ttextOriginal : " + reply["snippet"]["textOriginal"])
        print("\t\tlikeCount : " + str(reply["snippet"]["likeCount"]))
        print("\t\tpublishedAt : " + reply["snippet"]["publishedAt"])
        print("\t\tupdatedAt : " + reply["snippet"]["publishedAt"])
        print("\t\t-------------------------------------------------------------------")
    print("-------------------------------------------------------------------")


# Q1
def nombre_de_commentaire():
    print("nombre de commentaire : " + str(statistics["commentCount"]))


# Q2
def commentaire_le_plus_populaire_du_premier_Q1():
    likecount = 0
    commentaire = ""
    for snippet_c_user in snippet_c:
        if snippet_c_user["topLevelComment"]["snippet"]["likeCount"] > likecount:
            likecount = snippet_c_user["topLevelComment"]["snippet"]["likeCount"]
            commentaire = snippet_c_user["topLevelComment"]["snippet"]["textDisplay"]
    print("Nombre de j'aime : " + str(likecount))
    print("Texte  : " + commentaire)


# Q3 PHRASE NOMINAL
def dix_phrase_nominal_les_plus_frequent():
    commentaires = commentaire_de_mongodb()
    commentaires = (nettoyer_la_phrase(p) for p in commentaires)
    commentaires_dans_une_ligne = ""
    for c in commentaires:
        reshaped_text = arabic_reshaper.reshape(u'' + c)
        artext = get_display(reshaped_text)
        commentaires_dans_une_ligne += " " + artext.replace(".", " ")
    commentaires_dans_une_ligne = TextBlob(commentaires_dans_une_ligne)
    feature_count = dict()
    for phrase in commentaires_dans_une_ligne.noun_phrases:
        count = 0
        for word in phrase.split():
            if word not in stopwords.words('english'):
                count += commentaires_dans_une_ligne.words.count(word)
        feature_count[phrase] = count
    df = DataFrame().from_dict(list(feature_count.items()))
    df.columns = ['termes', 'frequence']
    df.sort_values('frequence', ascending=False, inplace=True)
    plt.style.use('ggplot')
    df.head(n=10).plot(x='termes', y='frequence', kind='bar')
    plt.show()


# Q3 TERME
def dix_terme_les_plus_frequent():
    comments = commentaire_de_mongodb()
    comments = (nettoyer_la_phrase(p) for p in comments)
    s = ""
    for c in comments:
        reshaped_text = arabic_reshaper.reshape(u'' + c)
        artext = get_display(reshaped_text)
        s += " " + artext.replace(".", " ")
    filtered_words = [word for word in s.split() if word not in stopwords.words('english')]
    wordcount = Counter(filtered_words)
    df = DataFrame.from_dict(wordcount, orient='index').reset_index().rename(
        columns={'index': 'termes', 0: 'frequence'})  # .set_index('word')
    df.sort_values('frequence', ascending=False, inplace=True)
    plt.style.use('ggplot')
    df.head(n=10).plot(x='termes', y='frequence', kind='bar')
    plt.show()


# Q3 N-GRAMS
def dix_ngrams_les_plus_frequent():
    comments = commentaire_de_mongodb()
    comments = (nettoyer_la_phrase(p) for p in comments)
    wordcount = dict()
    for c in comments:
        reshaped_text = arabic_reshaper.reshape(u'' + c)
        artext = get_display(reshaped_text)
        token = word_tokenize(artext.replace(".", ""))
        bigrams = ngrams(token, 2)
        for gram in bigrams:
            g = gram[0] + " " + gram[1]
            if g not in wordcount:
                wordcount[g] = 1
            else:
                wordcount[g] += 1
    # print(wordcount)
    df = DataFrame().from_dict(list(wordcount.items()))
    df.columns = ['termes', 'frequence']
    df.sort_values('frequence', ascending=False, inplace=True)
    plt.style.use('ggplot')
    df.head(n=10).plot(x='termes', y='frequence', kind='bar')
    plt.show()


def frequence_par_terme(terme=" "):
    comments = commentaire_de_mongodb()
    comments = (nettoyer_la_phrase(p) for p in comments)
    s = ""
    for c in comments:
        s += " " + c.replace(".", " ")
    filtered_words = [word for word in s.split() if word not in stopwords.words('english')]
    wordcount = Counter(filtered_words)
    freq = 0
    for k in wordcount.items():
        if k[0] == terme or k[0] in terme or terme in k[0]:
            freq += k[1]
    return freq


def frequence_cumul():
    comments = commentaire_de_mongodb()
    comments = (nettoyer_la_phrase(p) for p in comments)
    s = ""
    for c in comments:
        s += " " + c.replace(".", " ")
    filtered_words = [word for word in s.split() if word not in stopwords.words('english')]
    wordcount = Counter(filtered_words)
    freq_cum = 0
    for k in wordcount.items():
        freq_cum += k[1]
    return freq_cum


# Q4
def frequence_par_terme_en_entree(terme=" "):
    freq = frequence_par_terme(terme)
    print("a - fréquence dans le dataset traité ", str(freq))
    print("b - moyenne cette expression est citée dans un commentaire " + str(freq / int(MAX_RESULT)))


# Q5
def proba_conditionnel_A_sachant_B(E="", F=""):
    freq_cumul = frequence_cumul()
    freq_A = frequence_par_terme(E)
    freq_B = frequence_par_terme(F)
    if freq_A == 0:
        print("proba de B sachant A vaut : ", str("{0:.2f}".format(freq_B / freq_cumul)))
    else:
        prob_AB = (freq_B / freq_cumul) * (freq_A / freq_cumul)
        print("proba de B sachant A vaut : ", str("{0:.2f}".format(prob_AB / (freq_A / freq_cumul))))


# Q6
def pourcentage_sexe():
    f = 0
    u = 0
    m = 0
    x = ""
    for snippet_c_user in snippet_c:
        result = ''.join(
            [i for i in nettoyer_la_phrase(snippet_c_user["topLevelComment"]["snippet"]["authorDisplayName"]) if
             not i.isdigit()])
        if result.split(" ", 1)[1].replace(" ", "").replace(".", "") != "":
            x = result.split(" ", 1)[1].replace(" ", "").replace(".", "")
        else:
            x = "v"
        resp = gendre(result.split(" ", 1)[0].replace(".", ""), x).GET()
        if resp.json().get('gender') == "female":
            f += 1
        elif resp.json().get('gender') == "unknown":
            u += 1
        else:
            m += 1
    # print(f)
    # print(m)
    # print(u)
    pourcentagef = float("{0:.2f}".format((f / (int(MAX_RESULT))) * 100))
    pourcentagem = float("{0:.2f}".format((m / (int(MAX_RESULT))) * 100))
    pourcentageu = float("{0:.2f}".format((u / (int(MAX_RESULT))) * 100))
    print("pourcentage des commentaires publiés par les femmes : " + str(pourcentagef) + "%")
    print("pourcentage des commentaires publiés par les hommes : " + str(pourcentagem) + "%")
    print("pourcentage des commentaires publiés par les inconnus : " + str(pourcentageu) + "%")


# sentence_polarity
def sentiment_polarity_pour_chaque_commentaire():
    result = commentaire_de_mongodb()
    sentiment_scores = list()
    i = 0
    for sentence in result:
        line = TextBlob(sentence)
        sentiment_scores.append(line.sentiment.polarity)
        if i <= 10:
            i += 1
    occu = dict()
    for sent in sentiment_scores:
        count = 0
        sent = "{0:.2f}".format(sent)
        # print(sent)
        if sent not in occu:
            occu[sent] = 1
        else:
            occu[sent] += 1
    df = DataFrame().from_dict(occu, orient='index').reset_index().rename(columns={'index': 'polarity', 0: 'counter'})
    # print(df)
    plt.style.use('ggplot')
    df.plot(x='polarity', y='counter', kind='bar')
    plt.show()


if __name__ == "__main__":
    # id_video(id="Szysv8eGTr4")  # ARABE
    # id_video(id="RiNZl7tEeoQ")# LATIN
    # nombre_de_commentaire()
    # commentaire_le_plus_populaire_du_premier_Q1()
    # dix_terme_les_plus_frequent()
    # frequence_par_terme_en_entree(terme="الله")
    # proba_conditionnel_A_sachant_B(E="الله", F="يا رب")
    # pourcentage_sexe()
    print()
    # dix_ngrams_les_plus_frequent()
    # sentiment_polarity_pour_chaque_commentaire()
    # dix_terme_les_plus_frequent()
    dix_phrase_nominal_les_plus_frequent()
